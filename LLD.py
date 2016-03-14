import serial


class LLD:

    def __init__(self):
        #self.arduino = serial.Serial('/dev/tty.usbserial', 115000)
        self.setting = {}
        self.valve_setting = {}

        self.setting["Hot"]  = False
        self.setting["Mash"] = False
        self.setting["Boil"] = False

        self.valve_setting["Hot"]  = False
        self.valve_setting["Mash"] = False
        self.valve_setting["Boil"] = False

        self.pump_setting = False
        pass


    def set_duty(self, tank, cycle):
        if (self.setting[tank.tank_name] is True):
            #do something
            print tank.name + ": " + cycle
            pass


    def resistor_switch(self, tank, setting):
        if (setting is False):
            self.setting[tank.tank_name] = False
        else:
            self.setting[tank.tank_name] = True


    def valve_switch(self, tank, setting):
        if (setting is False):
            self.valve_setting[tank.tank_name] = False
        else:
            self.valve_setting[tank.tank_name] = True


    def pump_switch(self, setting):
        if setting is False:
            self.pump_setting  = False
        else:
            self.pump_setting = True


    def get_temperature(self, tank):

        if tank.tank_name == "Hot":
            return 56
        elif tank.tank_name == "Mash":
            return 70
        elif tank.tank_name == "Boil":
            return 80
        pass
