from __future__ import print_function
from builtins import input
from builtins import object
import unittest

from LLD import LLD
from Tank import Tank

class FakeTank(object):

    def __init__(self, name):
        self.tank_name = name

class LLDTest(unittest.TestCase):

    def setUp(self):
        self.lld = LLD()

        self.hot  = FakeTank("Hot")
        self.mash = FakeTank("Mash")
        self.boil = FakeTank("Boil")


    def check_one_resistor(self, tank):

        print("Set " + tank.tank_name + " at 20%")
        self.lld.set_resistor_duty(tank, 0.2)

        assert(input("Is tank " + tank.tank_name + " at 20 % ? [y/n]") == "y")

        print("Set " + tank.tank_name + " at 0%")
        self.lld.set_resistor_duty(tank, 0)

        assert(input("Is tank " + tank.tank_name + " at  0 % ? [y/n]") == "y")


    def test_resistor(self):
        ''' Check resistor duty cycle '''

        self.check_one_resistor(self.hot)
        self.check_one_resistor(self.mash)
        self.check_one_resistor(self.boil)


    def check_one_temperature(self, tank):

        temp = self.lld.get_temperature(tank)
        assert(input("Is tank " + tank.tank_name + " at "+ temp +"C ? [y/n]") == "y")


    def test_temperature(self):
        ''' Read temperatures '''

        t = self.lld.get_temperature(self.hot)
        assert(input("Is hot tank temp at " + str(t) + " ? [y/n]") == "y")
        t = self.lld.get_temperature(self.mash)
        assert(input("Is mash tank temp at " + str(t) + " ? [y/n]") == "y")
        t = self.lld.get_temperature(self.boil)
        assert(input("Is boil tank temp at " + str(t) + " ? [y/n]") == "y")

    def test_pump(self):
        ''' Test pump '''

        self.lld.pump_switch(True)
        assert(input("Is pump ON ? [y/n]") == "y")

        self.lld.pump_switch(False)
        assert(input("Is pump OFF ? [y/n]") == "y")

    def check_valve(self, tank):

        self.lld.valve_switch(tank, False)
        assert(input("Is valve "+ tank.tank_name +" OFF ? [y/n]") == "y")

        self.lld.valve_switch(tank, True)
        assert(input("Is valve "+tank.tank_name+" ON ? [y/n]") == "y")


    def test_valve(self):
        ''' Test valves '''

        self.check_valve(self.hot)
        self.check_valve(self.mash)
        #self.check_valve(self.boil)

    def check_one_dosage(self, tank):
        print("Start dosing 2 liters in "+ tank.tank_name)
        print("No message should appear before job is done....")

        self.lld.dose_water_blocking(tank, 2)
        assert(input("Do you have 2 liters in "+tank.tank_name+" ? [y/n]") == "y")



    def test_dosage(self):

        assert(input("This test will dose 2 liter per tank. Continue ? [y/n]") == "y")
        self.check_one_dosage(self.hot)
        self.check_one_dosage(self.mash)


if __name__ == '__main__':
    unittest.main()
