import threading 
import time

class List_max():

    def __init__(self, max_size):
        self.max_size = max_size
        self.array    = []

    def append(self, obj):
        if (len(self.array) >= self.max_size):
            self.array.remove(0)

        self.array.append(obj)



class History():
    """This class is made to manage temperature/power history"""



    def __init__(self):
        self.temperatures = List_max(10)
        self.powers       = List_max(10)
        
        t = threading.Timer(2, self.run)
        t.start()

        pass


    def run(self):
            
        print("ok")

        #self.temperatures.append(5)
        #self.powers.append(0)



if __name__ == '__main__':
    h = History()
    time.sleep(20)