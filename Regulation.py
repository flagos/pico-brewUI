

class Regulation:


    def __init__(self, hot, mash, boil):
        self.hot = hot
        self.mash = mash
        self.boil = boil
       
    def update_pid(self):
        self.hot.update_pid()
        self.mash.update_pid()
        self.boil.update_pid()
        
        max_duty = 1
    
        if (self.mash.output >= max_duty):
            self.lld.put("mash", max_duty)
            self.lld.put("boil", 0)
            self.lld.put("hot", 0)
        elif (self.mash.output + self.boil.output >= max_duty):
            self.lld.put("mash", self.mash.output)
            self.lld.put("boil", max_duty - self.mash.output)
            self.lld.put("hot", 0)
        elif (self.mash.output + self.boil.output + self.hot.output >= max_duty):
            self.lld.put("mash", self.mash.output)
            self.lld.put("boil", self.boil.output)
            self.lld.put("hot", self.hot.output)
        else:
            self.lld.put("mash", self.mash.output)
            self.lld.put("boil", self.boil.output)
            self.lld.put("hot", self.hot.output)
            
        
            
            
    