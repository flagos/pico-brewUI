import LLD

class Regulation:


    def __init__(self, hot, mash, boil):
        self.hot = hot
        self.mash = mash
        self.boil = boil
        self.lld = LLD.new()

    def update_pid(self):
        self.hot.update_pid()
        self.mash.update_pid()
        self.boil.update_pid()

        max_duty = 1

        hot  = self.hot
        mash = self.mash
        boil = self.boil

        if (self.mash.output >= max_duty):
            self.lld.duty(mash, max_duty)
            self.lld.duty(boil, 0)
            self.lld.duty(hot,  0)
        elif (self.mash.output + self.boil.output >= max_duty):
            self.lld.duty(mash, self.mash.output)
            self.lld.duty(boil, max_duty - self.mash.output)
            self.lld.duty(hot,  0)
        elif (self.mash.output + self.boil.output + self.hot.output >= max_duty):
            self.lld.duty(mash, self.mash.output)
            self.lld.duty(boil, self.boil.output)
            self.lld.duty(hot,  self.hot.output)
        else:
            self.lld.duty(mash, self.mash.output)
            self.lld.duty(boil, self.boil.output)
            self.lld.duty(hot,  self.hot.output)
