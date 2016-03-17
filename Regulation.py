from LLD import LLD
import time
import threading

class Regulation:


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


    def update_pid(self):
        hot  = self.hot
        mash = self.mash
        boil = self.boil

        lld = self.lld

        while True:

            hot.update_pid(lld.get_temperature(hot))
            mash.update_pid(lld.get_temperature(mash))
            boil.update_pid(lld.get_temperature(boil))

            max_duty = 1

            if (mash.output >= max_duty):
                lld.set_resistor_duty(mash, max_duty)
                lld.set_resistor_duty(boil, 0)
                lld.set_resistor_duty(hot,  0)
            elif (mash.output + boil.output >= max_duty):
                lld.set_resistor_duty(mash, mash.output)
                lld.set_resistor_duty(boil, max_duty - mash.output)
                lld.set_resistor_duty(hot,  0)
            elif (mash.output + boil.output + hot.output >= max_duty):
                lld.set_resistor_duty(mash, mash.output)
                lld.set_resistor_duty(boil, boil.output)
                lld.set_resistor_duty(hot,  max_duty - mash.output - boil.output)
            else:
                lld.set_resistor_duty(mash, mash.output)
                lld.set_resistor_duty(boil, boil.output)
                lld.set_resistor_duty(hot,  hot.output)

            time.sleep(self.sample_time)
