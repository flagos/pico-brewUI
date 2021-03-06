import serial
import time

from MessengerController import MessengerController


HOTPIN  = 0
MASHPIN = 1
BOILPIN = 2

MASH_VALVE_ON  = 11
MASH_VALVE_OFF = 12
HOT_VALVE      = 9

class LLD(MessengerController):
    '''
    Here is the driver class for our system. If you want to adapt it, you normally should only modify methods stating with an _, all the others methods should remain generic.
    '''

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

        self.cycles = (0, 0, 0)

        self.pump_setting = False
        self.set_pump(False)

        MessengerController.__init__(self)


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
        elif(tank.tank_name == "Hot"):
            pin = HOT_VALVE
            self.set_pin(pin, setting)

    def _pump(self, setting):
        pass

    def _dose_liters(self, tank, milliliters):
        self.flow_level_target += milliliters
        self._dose_liters(tank, True)

    def _wait_for_dosage(self, tank):
        while(self.flow_level_current < self.flow_level_target):
            time.sleep(0.02)
        self._dose_liters(tank, False)

    def _resistor_setting(self, cycles):
        for index, cycle in enumerate(cycles):
            if cycle is not None:
                self.cycles[index] = cycle
                
        self.set_resistors(int(self.cycles[0]*50)*2, int(self.cycles[1]*50)*2, int(self.cycles[2]*50)*2)
        

    def _ping_arduino(self):
        pass

    def set_resistors_duty(self, cycles):
        '''beware: order of tanks is mash, boil, hot for readibility'''
        if self.lock['resistor'] is True:
            self._resistor_setting(cycles)
            

    def set_pump(self, setting):
        if (self.lock['pump'] is True):
            self._pump(setting)

    def set_valve(self, tank, setting):
        if (self.lock['valve'] is True):
            self._valve(tank, setting)


    def resistor_switch(self, tank, setting):
        if (self.lock['resistor'] is False):
            if (setting is False):
                self.setting[tank.tank_name] = False
                cycles = (0, 0, 0)
                tanks_name = ("Mash", "Boil", "Hot")
                cycles[tanks_name.index(tank.tank_name)] = setting
                self.set_resistors_duty(cycles)
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
            self._pump(setting)
            if setting is False:
                self.pump_setting  = False
            else:
                self.pump_setting = True


    def get_temperature(self, tank):
        return self.temperature[tank.tank_name]


    def dose_water_blocking(self, tank, milliliters):
        self._dose_liters(tank, milliliters)
        self._wait_for_dosage(tank)


if __name__ == '__main__':
    lld = LLD()
