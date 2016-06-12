from threading import Thread
import time
from Tank import Tank

class MashTank(Thread, Tank):

    def __init__(self,hottank, boiltank, start_mash_queue, need_cleaning_queue, period=1, testing_queue_input=None, testing_queue_output=None):
        self.tank_name = "Mash"
        self.period = period
        self.hottank = hottank
        self.boiltank = boiltank
        self.start_mash_queue = start_mash_queue
        self.need_cleaning_queue = need_cleaning_queue
        self.testing_queue_input = testing_queue_input
        self.testing_queue_output = testing_queue_output

        self.mash_steps = []

        Thread.__init__(self, daemon=True)
        Tank.__init__(self)
        pass

    def push_steps(self, step):
        self.mash_steps.append(step)

    def run(self):
        while True:
            self.start_time=0
            self.boiltank_start_heating = False
            self.set_consign(None)

            self.need_cleaning_queue.put(None)
            self.need_cleaning_queue.join()
            
            self.start_mash_queue.get()  # wait for start

            step_number = 0

            while self.mash_steps:
                self.information("Mash " +str(step_number), "Not started")

                mash_step = self.mash_steps.pop(0)

                if(mash_step['water_volume']):
                    self.information(None, "adding "+ str(mash_step['water_volume']) + "mL")
                    self.hottank.pop_volume(mash_step['water_volume'])
                    self.current_volume = mash_step['water_volume']

                self.set_consign(mash_step['temperature'])

                while (self.read_temperature() < mash_step['temperature'] - 1):  # wait for temperature
                    time.sleep(self.period)
                    self.information(None, "waiting for temp")

                self.launch_chrono(mash_step["duration"])
                while self.is_over() is False:
                    time.sleep(self.period)
                    self.information(None, str(self.lasting()))
                    
                if('dump' in mash_step and mash_step['dump'] is True):
                    self.information("Mash Dumping #" + str(step_number), None)
                    self.set_consign(None)
                    if self.boiltank_start_heating is False:
                        self.boiltank.start_heat_queue.put(None)
                        
                        self.boiltank.start_heat_queue.join()    # wait for boil tank to be heating
                        self.boiltank_start_heating = True
                    self.set_consign(None)
                    self.dump_tank()
                    
                step_number += 1

            self.boiltank.start_counting_queue.put(None)
            self.start_mash_queue.task_done()
            pass

    def dump_tank(self):
        self.current_volume = 0
        pass
