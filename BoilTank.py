from threading import Thread
from Tank import Tank

import Queue
import time

class BoilTank(Thread, Tank):
    """ This class controls a BoilTank.
        This control is made with 3 Queues and 2 API
        - start heat will start heating even if there is not all liquid is the tank_in_use
        - start_boil will launch the boil process, task_done() when completed
        - need_cleaning will ask for a cleaning, waiting for a task_done()
        + add_boil_steps and
        + boiltank_programmed are for adding recipe at the rigth time
    """

    def __init__(self, start_heat_queue, start_boil_queue, start_counting_queue, need_cleaning_queue, period=1, testing_queue_input=None):

        self.tank_name = "Boil"
        self.period = period
        self.start_heat_queue     = start_heat_queue
        self.start_counting_queue = start_counting_queue
        self.start_boil_queue     = start_boil_queue
        self.need_cleaning_queue  = need_cleaning_queue
        self.testing_queue_input  = testing_queue_input
        self.boil_steps = []
        self.start_time = 0
        self.stop_time = 0
        self.period = period
        self.set_consign(None)

        self.running = True


        Thread.__init__(self)
        Tank.__init__(self)
        pass

    def add_boil_step(self, temperature, duration):
        self.boil_steps.append({'temperature':temperature, 'duration':duration})

    def run(self):
        self.set_consign(None)

        self.need_cleaning_queue.put(None)
        self.need_cleaning_queue.join()

        while (self.running):

            self.start_boil_queue.get() # boiltank has recipe

            self.start_heat_queue.get() # wait for enough water to boil
            self.set_consign(self.boil_steps[0]['temperature'])
            self.start_heat_queue.task_done()

            self.start_counting_queue.get() # start the counting boil steps
            while (self.boil_steps):
                boil_step = self.boil_steps.pop(0)

                self.set_consign(boil_step['temperature'])

                while self.read_temperature() + 2 < boil_step['temperature']:
                    time.sleep(self.period)

                self.launch_chrono(boil_step["duration"])
                while self.is_over() is False:
                    time.sleep(self.period)

                pass

            self.set_consign(None)
            self.start_chiller()

            self.stop_time = time.time()

            self.need_cleaning_queue.put(None)
            self.need_cleaning_queue.join()

            self.start_counting_queue.task_done()
            self.start_boil_queue.task_done()
            pass

    def start_chiller(self):
        pass


    def read_temperature(self):
        if self.testing_queue_input is not None:
            t = self.testing_queue_input.get()
            self.testing_queue_input.task_done()
            return t
        else:
            return self.feedback_value  # pragma: no cover
