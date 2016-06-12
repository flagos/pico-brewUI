from builtins import str
from builtins import object
import time
from datetime import timedelta, datetime
from PID import PID
from globals import MyGlobals
import os

SAMPLE_HISTORY = 10

class List_max(object):

    def __init__(self, max_size):
        self.max_size = max_size
        self.array    = []


    def append(self, obj):
        if (len(self.array) >= self.max_size):
            self.array.pop(0)

        self.array.append(obj)

class Chrono(object):

    def __init__(self):
        self.start_chrono = None
        self.start_pause  = None
        self.count        = 0



    def launch_chrono(self, duration):
        self.start_chrono = time.time()
        self.duration     = duration
        self.count        = 0


    def is_over(self):
        self.count += 1
        if os.getenv('CHRONO_DEBUG', "false") == "true" and self.count >= 3:
            return True
        if (self.start_pause is not None):
            return False
        elif(self.start_chrono is None):
            return True
        else:
            if (time.time() < self.start_chrono + self.duration):
                return False
            else:
                return True

    def pause(self):
        if (self.is_over()):
            return
        now              = time.time()
        self.start_pause = now
        self.lasting     = self.duration - (now - self.start_chrono)

    def resume(self):
        now = time.time()
        pause_duration = now - self.start_pause

        self.start_chrono += pause_duration

        self.start_pause = None  # keep this line last !
        # do not write here !

    def lasting(self):
        if (self.start_pause is not None):
            return self.lasting
        now = time.time()
        return int(self.duration - (now - self.start_chrono))


class Tank(PID, Chrono):

    def __init__(self):
        self.temperature_samples = []
        self.last_fill           = 0
        self.current_volume      = 0

        self.temperatures = List_max(SAMPLE_HISTORY)
        self.volumes      = List_max(SAMPLE_HISTORY)
        self.powers       = List_max(SAMPLE_HISTORY)
        self.timing       = List_max(SAMPLE_HISTORY)
        self.recipe_index = 0


        PID.__init__(self)
        Chrono.__init__(self)

    def update_pid(self, value):
        now  = time.time()
        nowd = datetime.now()
        if(now - self.last_fill > timedelta(minutes=5).seconds):
            self.last_fill = now
            self.temperatures.append(value)
            self.timing.append(str(nowd.hour) + ":" + str(nowd.minute))
            self.volumes.append(self.current_volume)

        #compute pid
        self.update(value)


    def read_temperature(self):
        if self.testing_queue_input is not None:
            t = self.testing_queue_input.get()
            self.testing_queue_input.task_done()
            return t
        else:
            return self.last_value  # pragma: no cover

    def information(self, msg, time):
        if MyGlobals.pico is not None:
            pico = MyGlobals.pico
            if msg is not None:
                pico.recipes[self.recipe_index].step = str(msg)
                
            if time is not None:
                pico.recipes[self.recipe_index].rem_time = str(time)
