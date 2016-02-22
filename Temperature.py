from threading import Thread
import time

class List_max(List):

    def __init__(self, max_size):
        self.max_size = max_size

    def append(self, obj):
        if (self.length() >= self.max_size):
            self.remove(0)

        super.append(obj)



class History(Thread):
    """This class is made to manage temperature/power history"""



    def __init__(self):
        self.temperatures = List_max(10)
        self.powers       = List_max(10)

        self.running = True

        Thread.__init__(self)
        pass


        def run(self):

            while(self.running):
                start_time = time.time()
                duration   = datetime(minutes=5)

                while(time.time() < start_time + duration):
                    time.sleep(3)

                self.temperatures.append(self.read_temperature())
                self.power.append(0)

            pass
