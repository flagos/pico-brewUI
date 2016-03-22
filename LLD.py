import serial

from MessengerController import Messengercontroller

class LLD(MessengerController):

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

        self.lock = {}
        self.lock["valve"]    = True
        self.lock["resistor"] = True
        self.lock["pump"]     = True

        self.pump_setting = False

        MessengerController.__init__(self)
        pass


    def _resistor_duty(self, tank, cycle):
        pass

    def _valve(self, tank, setting):
        pass

    def _pump(self, setting):
        pass

    def _update_temperature(self):
        pass

    def _dose_liters(self, tank, liters):
        pass

    def _wait_for_dosage(self, tank):
        pass

    def _ping_arduino(self):
        pass

    def set_resistor_duty(self, tank, cycle):
        if (self.setting[tank.tank_name] is True):
            self._resistor_duty(tank, cycle)


    def set_valve(self, setting):
        if (self.lock['valve'] is True):
            self._valve(tank, setting)

    def set_pump(self, setting):
        if (self.lock['pump'] is True):
            self._pump(setting)


    def resistor_switch(self, tank, setting):
        if (self.lock['resistor'] is False):
            if (setting is False):
                self.setting[tank.tank_name] = False
                return self._resistor_duty(tank, 0)
            else:
                self.setting[tank.tank_name] = True


    def valve_switch(self, tank, setting):
        if (self.lock['valve'] is False):
            if (setting is False):
                self.valve_setting[tank.tank_name] = False
            else:
                self.valve_setting[tank.tank_name] = True


    def pump_switch(self, setting):
        if (self.lock['pump'] is False):
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

    def dose_water_blocking(self, tank, liters):
        self._dose_liters(tank, liters)
        self._wait_for_dosage(liters)




if __name__ == "__main__":
    lld = LLD()
    lld._
