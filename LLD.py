import serial
import time

from MessengerController import MessengerController


HOTPIN  = 0
MASHPIN = 1
BOILPIN = 2

MASH_VALVE_ON  = 11
MASH_VALVE_OFF = 12
HOT_VALVE = 5

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

        self.resistor_duty = {}
        self.resistor_duty["Hot"] = 0
        self.resistor_duty["Mash"] = 0
        self.resistor_duty["Boil"] = 0

        self.pump_setting = False

        MessengerController.__init__(self)


    def _resistor_duty(self, tank, cycle):
        tank.resistor_duty = cycle
        if(tank.tank_name == "Hot"):
            self.set_pwm_pin(HOTPIN, cycle)
        elif (tank.tank_name == "Mash"):
            self.set_pwm_pin(MASHPIN, cycle)
        elif (tank.tank_name == "Boil"):
            self.set_pwm_pin(BOILPIN, cycle)


    def _valve(self, tank, setting):
        if(tank.tank_name == "Mash"):
            pin = 0
            if setting is True:
                pin = MASH_VALVE_ON
            else:
                pin = MASH_VALVE_OFF

            self.set_pin(pin, True)
            time.sleep(7)  # will freeze UI :-/
            self.set_pin(pin, False)


    def _pump(self, setting):
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
            self._valve(tank, setting)
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
            return self.temperature["Hot"]
        elif tank.tank_name == "Mash":
            return self.temperature["Mash"]
        elif tank.tank_name == "Boil":
            return self.temperature["Boil"]

    def dose_water_blocking(self, tank, liters):
        self._dose_liters(tank, liters)
        self._wait_for_dosage(liters)


if __name__ == '__main__':
    lld = LLD()
