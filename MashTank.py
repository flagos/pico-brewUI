from threading import Thread
import time

class MashTank(Thread):

    def __init__(self,hottank, boiltank,  period=1,  testing_queue_input=None, testing_queue_output=None):
        self.period = period
        self.hottank = hottank
        self.boiltank = boiltank
        self.testing_queue_input = testing_queue_input
        self.testing_queue_output = testing_queue_output

        self.mash_steps = []
        self.start_time=0
        self.stop_time=0
        self.tank_in_use = False

        Thread.__init__(self)
        pass

    def add_mash_step(self, temperature=None, duration=None, name=None, water_volume=None):
        self.mash_steps.append({'temperature': temperature, 'duration':duration, 'name':name, 'water_volume':water_volume})
        pass

    def start_mash(self):
        self.tank_in_use = True


    def run(self):
        while (not self.tank_in_use):
            time.sleep(self.period)

        while self.mash_steps:
            mash_step = self.mash_steps.pop(0)

            if(mash_step['water_volume']):
                self.hottank.pop_volume(mash_step['water_volume'])

            self.set_consign(mash_step['temperature'])

            while (self.read_temperature() < mash_step['temperature'] - 1): # wait for temperature
                time.sleep(self.period)

            self.start_time = time.time()
            while (time.time() < self.start_time + mash_step['duration']):
                time.sleep(self.period)
            pass

        self.stop_time = time.time()
        while not self.boiltank.is_ready():
            time.sleep(self.period)

        self.dump_tank()
        self.tank_in_use = False
        pass

    def is_tank_in_use(self):
        return self.tank_in_use

    def set_consign(self, temperature):
        pass

    def read_temperature(self):
        if self.testing_queue_input is not None:
            return self.testing_queue_input.get()
        else:
            return 55

    def dump_tank(self):
        pass
