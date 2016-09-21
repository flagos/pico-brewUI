from LLD import *
import csv

SAMPLING_PERIOD = 15
MAX_DUTY = 1800/3200
lld = LLD()


class Fake_Tank(object):

    def __init__(self, name):
        self.resistor_duty = 0
        self.tank_name = name



hot = Fake_Tank("Hot")
mash = Fake_Tank("Mash")
boil = Fake_Tank("Boil")
tanks = (mash, boil, hot)
tut = boil  # for tank under test

lld.set_resistors_duty(tanks, (0,MAX_DUTY,0))

time.sleep(3)

with open('pid_calib.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["Setting","Temperature"])


    t = lld.get_temperature(tut)
    while(t < 90):
        csvwriter.writerow(["1",t])
        print(t)
        time.sleep(SAMPLING_PERIOD)
        t = lld.get_temperature(tut)

    lld.set_resistors_duty(tanks, (0, 0, 0))
    i = 0
    while (i < SAMPLING_PERIOD * 4 * 15):
        t = lld.get_temperature(tut)
        csvwriter.writerow(["1",t])
        print(t)
        time.sleep(SAMPLING_PERIOD)


        
print("calib test is done, take care of hot water")
