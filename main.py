import time
import defs as og
import random as rd

from autopilot.input import Mouse
from autopilot.input import Keyboard
m = Mouse.create()
k = Keyboard.create()


max_position = (955, 430)
#max_position = (955, 412)
#max_position = (955, 392)
#max_position = (955, 372)
first_ok = (887, 474)
first_ok = (892, 452)
first_ok = (892, max_position[1] + 40)
overview = (138, 214)
fleet = (149, 289)
galaxy = (161, 314)
objective = "1:196:8"
second_ok = (897, 421)
third_ok = (884, 398)
attack_button = (737, 305)
first_field_fleet = (941, 252)

low_wait = 0.8
counter = 0




class Job:
    def __init__(self, reports_string, mouse, keyboard):
        self.reports = []
        self.mouse = mouse
        self.keyboard = keyboard
        ls = []
        for line in reports_string.split('\n'):
            if 'Chance of counter-espionage:' not in line:
                ls.append(line)
            else:
                self.reports.append(og.Report('\n'.join(ls)))
                ls = []
    
    def defenseless(self):
        return [report for report in self.reports if not report.has_defense()]

    def attack(self, report):
        coords = report.get_coordinates()
        self.mouse.move(*fleet)
        self.mouse.click()
        time.sleep(low_wait)
        self.mouse.move(*max_position)
        self.mouse.click()
        self.mouse.move(*first_ok)
        self.mouse.click()
        time.sleep(low_wait)
        self.mouse.move(*first_field_fleet)
        self.mouse.click()
        self.keyboard.type('\b')
        self.keyboard.type(str(coords.get_galaxy()), delay = 0.05)
        self.keyboard.type('\t', delay = 0)
        self.keyboard.type(str(coords.get_solar_system()), delay = 0.05)
        self.keyboard.type('\t')
        self.keyboard.type(str(coords.get_position()), delay = 0.05)
        self.keyboard.press_and_release('Enter', delay = 0)
        time.sleep(low_wait)
        self.mouse.move(*attack_button)
        self.mouse.click()
        self.keyboard.press_and_release('Enter', delay = 0)
        time.sleep(low_wait)
        self.mouse.move(*overview)
        self.mouse.click()

    
    def farm(self, planet_coordinates_string, combustion):
        planet_coordinates = og.Coordinates(planet_coordinates_string)
        for report in sorted(self.reports, key = lambda x: x.get_coordinates().distance(planet_coordinates)):
            self.attack(report)
            time.sleep(2 * report.get_coordinates().get_probe_time(planet_coordinates, 5) + 2.5)




    

s = """     
Resources on Cerova City [1:197:5] at 09-17 20:10:47
Metal:  20.690  Crystal:    3.352
Deuterium:  537     Energy: 2.324
Your espionage does not show abnormalities in the atmosphere of the planet. There appears to have been no activity on the planet within the last hour.
Fleets
Defense
Chance of counter-espionage:0%
    
Resources on Homeworld [1:196:8] at 09-17 20:12:34
Metal:  4.172   Crystal:    1.334
Deuterium:  387     Energy: 897
Your espionage shows abnormalities in the atmosphere of the planet which suggests a activity within the last 15 minutes.
Fleets
Defense
Chance of counter-espionage:0%"""


a = Job(s, m, k)
a.farm("1:199:10", 5)
            




