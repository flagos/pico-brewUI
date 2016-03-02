import serial


class LLD:

    def __init__(self):
        self.arduino = serial.Serial('/dev/tty.usbserial', 115000)
        self.setting = {}

        self.setting["Hot"]  = False
        self.setting["Mash"] = False
        self.setting["Boil"] = False


        self.setting["Hot"]  = True
        self.setting["Mash"] = True
        self.setting["Boil"] = True


        pass


    def set_duty(self, tank, cycle):
        if (self.setting[tank.name] is True):
            #do something
            print tank.name + ": " + cycle
            pass


    def switch(self, tank, setting):
        if (setting is False):
            self.setting[tank.name] = False
        else:
            self.setting[tank.name] = True
