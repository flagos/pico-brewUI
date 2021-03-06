#!/usr/bin/python
# sendandreceivearguments.py
# Author: Adrien Emery
# Make sure the you have the SendAndReceiveArguments example loaded onto the Arduino
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
import random
import sys
import serial
import time
import threading

from globals import MyGlobals
from cmdmessenger import CmdMessenger
from serial.tools import list_ports




class MessengerController(object):

    def __init__(self):

        # make sure this baudrate matches the baudrate on the Arduino
        self.running = False
        self.baud = 9600
        self.temperature = {}
        self.temperature["Hot"]  = 100
        self.temperature["Mash"] = 100
        self.temperature["Boil"] = 100

        self.flow_level_current = 0
        self.flow_level_target  = 0

        self.commands = ['acknowledge',
                         'error',
                         'ping',
                         'SetPin',
                         'PwmPin',
                         'ReadTemperature',
                         'ReadFlow',
                         'Resistor'
                         ]

        if (MyGlobals.args['hardware_disconnected'] is False):
            try:
                # try to open the first available usb port
                self.port_name = self.list_usb_ports()[0][0]
                self.serial_port = serial.Serial(self.port_name, self.baud, timeout=0, rtscts=True)
            except (serial.SerialException, IndexError):
                raise SystemExit('Could not open serial port.')
            else:
                time.sleep(2)
                self.messenger = CmdMessenger(self.serial_port)

            # send a command that the arduino will acknowledge
            self.messenger.send_cmd(self.commands.index('acknowledge'))
            # Wait until the arduino sends and acknowledgement back
            status = self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'), timeout=5)
            if (status is None):
                print('Arduino timeout')
                sys.exit(255)

            # attach callbacks
            self.messenger.attach(func=self.on_error, msgid=self.commands.index('error'))
            self.messenger.attach(func=self.on_read_temperature,
                                  msgid=self.commands.index('ReadTemperature'))
            self.messenger.attach(func=self.on_read_flow,
                                  msgid=self.commands.index('ReadFlow'))


            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution



    def list_usb_ports(self):
        """ Use the grep generator to get a list of all USB ports.
        """
        ports = [port for port in list_ports.grep('USB')]
        return ports

    def on_error(self, received_command, *args, **kwargs):
        """Callback function to handle errors
        """
        print(('Error:', args[0][0]))

    def on_read_temperature(self, received_command, *args, **kwargs):
        """ Callback on temperature """

        self.temperature["Hot"]  = int(args[0][0])/100
        self.temperature["Mash"] = int(args[0][1])/100
        self.temperature["Boil"] = int(args[0][2])/100

    def on_read_flow(self, received_command, *args, **kwargs):
        """ Callback on flow """

        self.flow_level_current = int(args[0][0])


    def stop(self):
        self.running = False

    def ping(self):
        """ Send a ping (blocking) """
        self.messenger.send_cmd(self.commands.index('ping'))

        self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'))

    def set_pin(self, pin, value):
        """ Set a boolean value to a pin (blocking) """
        self.messenger.send_cmd(self.commands.index('SetPin'), pin, value)

        self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'))

    def set_pwm_pin(self, pin, value):
        """ Set a pwm value to a pin (blocking)
            value is supposed to be between 0-1
        """
        self.messenger.send_cmd(self.commands.index('PwmPin'), pin, int(value*255))

        self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'))

    def set_resistors(self, mash, boil, hot):
        if (MyGlobals.args['hardware_disconnected'] is False):
            self.messenger.send_cmd(self.commands.index('Resistor'), hot, mash, boil, 100 - mash - boil - hot)


    def dump_in_water(self, valve, value):
        """ Set a pwm value to a pin (blocking)
            value is supposed to be between 0-65 liters
        """
        self.messenger.send_cmd(self.commands.index('DumpInWater'), valve, value)
        self.valve_status[valve] = True
        self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'))



    def run(self):
        """Main loop to send and receive data from the Arduino
        """
        while (True):
            self.messenger.feed_in_data()
            time.sleep(0.01)  # please do not hurt my core

if __name__ == '__main__':
    msg = MessengerController()

    try:
        print('Press Ctrl+C to exit...')
        msg.run()
    except KeyboardInterrupt:
        #msg.stop()
        msg.set_pwm_pin(5, 0.5)
        print('Exiting...')
        time.sleep(100)
