from threading import Thread
import time

class MashTank(Thread):

    def __init__(self,hottank, boiltank, start_mash_queue, need_cleaning_queue,  period=1,  testing_queue_input=None, testing_queue_output=None):
        self.period = period
        self.hottank = hottank
        self.boiltank = boiltank
        self.start_mash_queue = start_mash_queue
        self.need_cleaning_queue = need_cleaning_queue
        self.testing_queue_input = testing_queue_input
        self.testing_queue_output = testing_queue_output
        self.stop_time = 0

        self.mash_steps = []

        Thread.__init__(self)
        pass

    def add_mash_step(self, temperature=None, duration=None, name=None, water_volume=None, dump=False):
        self.mash_steps.append({'temperature': temperature, 'duration':duration, 'name':name, 'water_volume':water_volume, 'dump':dump})
        pass



    def run(self):

        while 1:
            self.start_time=0
            self.stop_time=0
            self.boiltank_start_heating = False

            self.need_cleaning_queue.put(None)
            self.need_cleaning_queue.join()

            self.start_mash_queue.get() # wait for start

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

                if(mash_step['dump'] is True):
                    self.set_consign(None)
                    if self.boiltank_start_heating is False:
                        self.boiltank.start_heat_queue.put(None)
                        self.boiltank.start_heat_queue.join()    # wait for boil tank to be heating
                        self.boiltank_start_heating = True
                    self.dump_tank()
                pass

            self.boiltank.start_counting_queue.put(None)
            self.start_mash_queue.task_done()
            pass
        pass

    def set_consign(self, temperature):
        pass

    def read_temperature(self):
        if self.testing_queue_input is not None:
            return self.testing_queue_input.get()
        else:
            return 55

    def dump_tank(self):
        pass
