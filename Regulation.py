import LLD
import time
from threading import Timer

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
        Timer(self.sample_time, self.update_pid, ()).start()

    def update_pid(self):
        hot  = self.hot
        mash = self.mash
        boil = self.boil

        lld = self.lld

        hot.update_pid(lld.get_temperature(hot))
        mash.update_pid(lld.get_temperature(mash))
        boil.update_pid(lld.get_temperature(boil))

        max_duty = 1

        if (mash.output >= max_duty):
            lld.set_duty(mash, max_duty)
            lld.set_duty(boil, 0)
            lld.set_duty(hot,  0)
        elif (mash.output + boil.output >= max_duty):
            lld.set_duty(mash, mash.output)
            lld.set_duty(boil, max_duty - mash.output)
            lld.set_duty(hot,  0)
        elif (mash.output + boil.output + hot.output >= max_duty):
            lld.set_duty(mash, mash.output)
            lld.set_duty(boil, boil.output)
            lld.set_duty(hot,  max_duty - mash.output - boil.output)
        else:
            lld.set_duty(mash, mash.output)
            lld.set_duty(boil, boil.output)
            lld.set_duty(hot,  hot.output)
