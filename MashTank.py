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

        Thread.__init__(self, daemon=True)
        Tank.__init__(self)
        pass

    def get_step(self):
        return self.pico.recipes[self.recipe_index].mash_steps[self.step_number]

    def run(self):
        while True:
            self.start_time=0
            self.boiltank_start_heating = False
            self.set_consign(None)

            self.need_cleaning_queue.put(None)
            self.need_cleaning_queue.join()
            
            self.start_mash_queue.get()  # wait for start

            self.step_number = 0

            while self.step_number < len(self.pico.recipes[self.recipe_index].mash_steps):
                self.information("Mash " +str(self.step_number), "Not started")

                if(self.get_step()['water_volume']):
                    self.information(None, "adding "+ str(self.get_step()['water_volume']) + "mL")
                    self.hottank.pop_volume(self.get_step()['water_volume'])
                    self.current_volume = self.get_step()['water_volume']

                self.set_consign(self.get_step()['temperature'])

                while (self.read_temperature() < self.get_step()['temperature'] - 1):  # wait for temperature
                    time.sleep(self.period)
                    self.information(None, "waiting for temp")

                self.launch_chrono(self.get_step()["duration"])
                while self.is_over() is False:
                    time.sleep(self.period)
                    self.information(None, str(self.lasting()))
                    
                if('dump' in self.get_step() and self.get_step()['dump'] is True):
                    self.information("Mash Dumping #" + str(self.step_number), None)
                    self.set_consign(None)
                    if self.boiltank_start_heating is False:
                        self.boiltank.start_heat_queue.put(None)
                        
                        self.boiltank.start_heat_queue.join()    # wait for boil tank to be heating
                        self.boiltank_start_heating = True
                    self.set_consign(None)
                    self.dump_tank()
                    
                self.step_number += 1

            self.boiltank.start_counting_queue.put(None)
            self.start_mash_queue.task_done()

    def dump_tank(self):
        self.current_volume = 0
