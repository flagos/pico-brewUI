#!/usr/bin/python
# sendandreceivearguments.py
# Author: Adrien Emery
# Make sure the you have the SendAndReceiveArguments example loaded onto the Arduino
import random
import sys
import serial
import time

from cmdmessenger import CmdMessenger
from serial.tools import list_ports


class MessengerController(object):

    def __init__(self):
        # make sure this baudrate matches the baudrate on the Arduino
        self.running = False
        self.baud = 115200
        self.temperature = {}
        self.valve_status = []
        self.commands = ['acknowledge',
                         'error',
                         'ping',
                         'SetPin',
                         'PwmPin'              ,
                         'ReadTemperature'     ,
                         'DumpInWater'         ,
                         'DumpInWater_reached'
                         ]

        try:
            # try to open the first available usb port
            self.port_name = '/dev/ttyUSB0'
            self.serial_port = serial.Serial(self.port_name, self.baud, timeout=0, rtscts=True)
        except (serial.SerialException, IndexError):
            raise SystemExit('Could not open serial port.')
        else:
            self.messenger = CmdMessenger(self.serial_port)
            # attach callbacks
            self.messenger.attach(func=self.on_error, msgid=self.commands.index('error'))
            self.messenger.attach(func=self.on_read_temperature,
                                  msgid=self.commands.index('ReadTemperature'))
            self.messenger.attach(func=self.on_dump_in_reached,
                                  msgid=self.commands.index('DumpInWater_reached'))

            # send a command that the arduino will acknowledge
            self.messenger.send_cmd(self.commands.index('acknowledge'))
            # Wait until the arduino sends and acknowledgement back
            self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'))

    def list_usb_ports(self):
        """ Use the grep generator to get a list of all USB ports.
        """
        ports =  [port for port in list_ports.grep('USB')]
        return ports

    def on_error(self, received_command, *args, **kwargs):
        """Callback function to handle errors
        """
        print('Error:', args[0][0])

    def on_read_temperature(self,  received_command, *args, **kwargs):
        """ Callback on temperature """

        self.temperature["Hot"]  = args[0][0]
        self.temperature["Mash"] = args[0][1]
        self.temperature["Boil"] = args[0][2]

    def on_dump_in_reached(self,  received_command, *args, **kwargs):
        """ Callback on dump_in reached """

        self.valve_status[args[0][0]] = False


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

        self.messenger.send_cmd(self.commands.index('ping'))

        self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'))

        # Check to see if any data has been received
        #self.messenger.feed_in_data()


if __name__ == '__main__':
    msg = MessengerController()

    try:
        print('Press Ctrl+C to exit...')
        print()
        msg.run()
    except KeyboardInterrupt:
        msg.stop()
        print('Exiting...')
