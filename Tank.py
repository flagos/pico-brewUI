import time
from datetime import timedelta, datetime
from PID import PID

SAMPLE_HISTORY = 10

class List_max():

    def __init__(self, max_size):
        self.max_size = max_size
        self.array    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def append(self, obj):
        if (len(self.array) >= self.max_size):
            self.array.pop(0)

        self.array.append(obj)


class Tank(PID):

    def __init__(self):
        self.temperature_samples = []
        self.last_fill = 0

        self.temperatures = List_max(SAMPLE_HISTORY)
        self.powers       = List_max(SAMPLE_HISTORY)
        self.timing       = List_max(SAMPLE_HISTORY)


        PID.__init__(self)


    def update_pid(self, value):
        now  = time.time()
        nowd = datetime.now()
        if(now - self.last_fill > timedelta(minutes=5).seconds):
            self.last_fill = now
            self.temperatures.append(value)
            self.timing.append(str(nowd.hour) + ":" + str(nowd.minute))

        #compute pid
        self.update(value)
