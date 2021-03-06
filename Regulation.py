from future import standard_library
standard_library.install_aliases()
from builtins import object
from LLD import LLD
import time
import threading

class Regulation(object):


    def __init__(self, hot, mash, boil):
        self.hot  = hot
        self.mash = mash
        self.boil = boil
        self.lld  = LLD()

        self.sample_time = 5
        hot.setSampleTime(self.sample_time)
        mash.setSampleTime(self.sample_time)
        boil.setSampleTime(self.sample_time)
        thread = threading.Thread(target=self.update_pid, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def set_resistors(self, tanks, cycles):
        tanks[0].resistor_duty = cycles[0]
        tanks[1].resistor_duty = cycles[1]
        tanks[2].resistor_duty = cycles[2]
        self.lld.set_resistors_duty(cycles)

    def update_pid(self):
        hot  = self.hot
        mash = self.mash
        boil = self.boil
        tanks = (mash, boil, hot)
        
        lld = self.lld

        while True:

            hot.update_pid(lld.get_temperature(hot))
            mash.update_pid(lld.get_temperature(mash))
            boil.update_pid(lld.get_temperature(boil))

            max_duty = 1

            if (mash.output >= max_duty):
                self.set_resistors(tanks, (max_duty, 0, 0))
            elif (mash.output + boil.output >= max_duty):
                self.set_resistors(tanks, (mash.output, max_duty - mash.output, 0))
            elif (mash.output + boil.output + hot.output >= max_duty):
                self.set_resistors(tanks, (mash.output, boil.output, max_duty - mash.output - boil.output))
            else:
                self.set_resistors(tanks, (mash.output, boil.output, hot.output))

            time.sleep(self.sample_time)
