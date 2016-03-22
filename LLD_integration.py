import unittest

from LLD import LLD
from Tank import Tank

class FakeTank:

    def __init__(self, name):
        self.name = name

class LLDTest(unittest.TestCase):

    def setUp(self):
        self.lld = LLD.LLD()

        self.hot  = FakeTank("Hot")
        self.mash = FakeTank("Mash")
        self.boil = FakeTank("Boil")


    def check_one_resistor(self, tank):

        print("Set " + tank.name + " at 20%")
        lld.set_resistor_duty(tank, 0.2)

        assert(raw_input("Is tank " + tank.name + " at 20 % ? [y/n]") == "y")

        print("Set " + tank.name + " at 0%")
        lld.set_resistor_duty(tank, 0)

        assert(raw_input("Is tank " + tank.name + " at  0 % ? [y/n]") == "y")


    def test_resistor(self):
        ''' Check resistor duty cycle '''

        self.check_one_resistor(self.hot)
        self.check_one_resistor(self.mash)
        self.check_one_resistor(self.boil)


    def check_one_temperature(self, tank):

        temp = self.lld.get_temperature(tank)
        assert(raw_input("Is tank " + tank.name + " at "+ temp +"°C ? [y/n]") == "y")


    def test_temperature(self):
        ''' Read temperatures '''

        self.lld.get_temperature(self.hot)
        self.lld.get_temperature(self.mash)
        self.lld.get_temperature(self.boil)

    def test_pump(self):
        ''' Test pump '''

        self.lld.pump_switch(True)
        assert(raw_input("Is pump ON ? [y/n]") == "y")

        self.lld.pump_switch(False)
        assert(raw_input("Is pump OFF ? [y/n]") == "y")

    def check_valve(self, tank):

        self.lld.valve_switch(tank, True)
        assert(raw_input("Is valve "+ tank.name +" OFF ? [y/n]") == "y")

        self.lld.valve_switch(tank, True)
        assert(raw_input("Is valve "+tank.name+" ON ? [y/n]") == "y")


    def test_valve(self):
        ''' Test valves '''

        self.check_valve(self.hot)
        self.check_valve(self.mash)
        self.check_valve(self.boil)

    def check_one_dosage(self, tank):
        print("Start dosing 2 liters in "+ tank.name)
        print("No message should appear before job is done....")

        lld.dose_water_blocking(tank, 2)
        assert(raw_input("Do you have 2 liters in "+tank.name+" ? [y/n]") == "y")



    def test_dosage(self):

        assert(raw_input("This test will dose 2 liter per tank. Continue ? [y/n]") == "y")
        self.check_one_dosage(self.hot)
        self.check_one_dosage(self.mash)
