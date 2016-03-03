import time
from datetime import timedelta
from PID import PID


class List_max():

    def __init__(self, max_size):
        self.max_size = max_size
        self.array    = []

    def append(self, obj):
        if (len(self.array) >= self.max_size):
            self.array.remove(0)

        self.array.append(obj)


class Tank(PID):

    def __init__(self):
        self.temperature_samples = []
        self.last_fill = 0

        self.temperatures = List_max(10)
        self.powers       = List_max(10)

        PID.__init__(self)


    def update_pid(self, value):
        now = time.time()
        if(now - self.last_fill > timedelta(minutes=5).seconds):
            self.last_fill = now
            self.temperatures.append(value)

        #compute pid
        self.update(value)
