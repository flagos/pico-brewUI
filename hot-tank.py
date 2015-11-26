from threading import Thread
import time

class HotTank(Thread):

    def __init__(self):
        self.current_volume = 0
        self.target_volume = 0
        Thread.__init__(self)
        pass

    def push_volume(self, vol):
        self.target_volume += vol
        print "push "+str(vol)+" L"
        pass


    def pop_volume(self, vol):
        self.current_volume -= vol
        self.target_volume  -= vol
        pass

    def add_liters(self, vol):
        #blocking call till the volume is not present
        self.current_volume += vol
        print "add "+str(vol)+" L current_volume: "+str(self.current_volume)
        pass

    def set_consign(self, temperature):
        pass


    def read_temperature(self):
        return 55

    def run(self):
        while 1:
            if (self.current_volume < self.target_volume):
                if (self.current_volume == 0):
                    self.add_liters(10)
                else:
                    if(self.read_temperature()>=54):
                        self.add_liters(1)

                self.set_consign(55)
            else:
                print "tank filled"
            time.sleep(1)
            pass
        pass



tank_thread = HotTank()
tank_thread.start()

tank_thread.push_volume(20)
tank_thread.join()
