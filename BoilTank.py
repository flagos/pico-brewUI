from threading import Thread
import time

class BoilTank(Thread):

    def __init__(self, start_heat_queue, start_boil_queue, period=1, testing_queue_input=None):
        self.period = period
        self.start_heat_queue    = start_heat_queue
        self.start_boil_queue    = start_boil_queue
        self.testing_queue_input = testing_queue_input
        self.is_ready = False
        self.boil_steps = []
        self.start_time = 0
        self.stop_time = 0
        self.period = period
        self.set_consign(None)

        Thread.__init__(self)
        pass


    def set_tank_ready(self):
        self.is_ready = True
        pass

    def add_boil_step(self, temperature, duration):
        self.boil_steps.append({'temperature':temperature, 'duration':duration})

    def run(self):
        self.set_consign(None)
        while 1:
            self.start_heat_queue.get() # wait for enough water to boil
            self.set_consign(self.boil_steps[0]['temperature'])
            self.start_heat_queue.task_done()

            self.start_boil_queue.get() # start the boil steps
            while (self.boil_steps):
                boil_step = self.boil_steps.pop(0)

                self.set_consign(boil_step['temperature'])

                while self.read_temperature() + 2 < boil_step['temperature']:
                    time.sleep(self.period)

                self.start_time = time.time()
                while time.time() < self.start_time + boil_step['duration']:
                    time.sleep(self.period)

                pass

            self.start_chiller()

            self.stop_time = time.time()

            # wait for clean....

            self.start_boil_queue.task_done()
            pass
        pass

    def start_chiller(self):
        pass


    def read_temperature(self):
        if self.testing_queue_input is not None:
            t = self.testing_queue_input.get()
            self.testing_queue_input.task_done()
            return t
        else:
            return 55
            pass
        pass

    def set_consign(self, arg):
        self.consign = arg
        pass
