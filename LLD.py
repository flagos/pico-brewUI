import serial


class LLD:

    def __init__(self):
        #self.arduino = serial.Serial('/dev/tty.usbserial', 115000)
        self.setting = {}

        self.setting["Hot"]  = False
        self.setting["Mash"] = False
        self.setting["Boil"] = False
        pass


    def set_duty(self, tank, cycle):
        if (self.setting[tank.tank_name] is True):
            #do something
            print tank.name + ": " + cycle
            pass


    def switch(self, tank, setting):
        if (setting is False):
            self.setting[tank.tank_name] = False
        else:
            self.setting[tank.tank_name] = True

    def get_temperature(self, tank):
        pass
