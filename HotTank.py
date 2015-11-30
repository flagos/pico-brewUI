from threading import Thread
import time

class HotTank(Thread):

    def __init__(self, saturation = 50, period=1, testing_queue_input=None, testing_queue_output=None):
        self.current_volume = 0
        self.target_volume = 0
        self.period = period
        self.testing_queue_input = testing_queue_input
        self.testing_queue_output = testing_queue_output
        self.saturation = saturation
        self.temperature_order = 55  # be safe
        Thread.__init__(self)
        pass

    def push_volume(self, vol):
        self.target_volume += vol
        pass


    def pop_volume(self, vol):
        self.current_volume -= vol
        self.target_volume  -= vol
        pass

    def add_liters(self, vol):
        #blocking call till the volume is not present
        self.current_volume += vol
        #print "add "+str(vol)+" L current_volume: "+str(self.current_volume)
        pass

    def set_consign(self, temperature):
        pass


    def read_temperature(self):
        if self.testing_queue_input is not None:
            return self.testing_queue_input.get()
        else:
            return 55

    def run(self):
        while 1:
            temperature = self.read_temperature()
            if (self.current_volume < self.target_volume):
                if (self.current_volume == 0):
                    self.add_liters(10)
                else:
                    if(temperature>=self.temperature_order - 1):
                        if (self.current_volume < self.saturation):
                            self.add_liters(1)

                self.set_consign(self.temperature_order)
            else:
                pass

            if self.testing_queue_output is not None:
                self.testing_queue_output.put(self.current_volume)
            time.sleep(self.period)
            pass
        pass
