import re
import math


def all_buildings():
    return ['Metal Mine', 'Crystal Mine', 'Deuterium Synthesizer',
        'Solar Plant', 'Fusion Reactor', 'Robotics Factory',
        'Nanite Factory', 'Shipyard', 'Metal Storage', 'Crystal Storage',
        'Deuterium Tank', 'Research Lab', 'Terraformer', 'Missile Silo',
        'Lunar Base', 'Sensor Phalanx', 'Jump Gate']

def all_ships():
    return ['Small Cargo', 'Large Cargo', 'Light Fighter', 'Heavy Fighter',
            'Cruiser', 'Battleship', 'Colony Ship', 'Recycler', 'Espionage Probe',
            'Bomber', 'Solar Satellite', 'Destroyer', 'Deathstar']

def all_ships_properties():
    """
    Return all of the ship's properties as a dictionary
    """
    pass


def all_research():
    return ['Espionage Technology', 'Computer Technology', 'Weapons Techonology',
            'Shielding Techonology', 'Armour Technology', 'Energy Technology',
            'Hyperspace Technology', 'Combustion Drive', 'Impulse Drive',
            'Hyperspace Drive', 'Laser Technology', 'Ion Technology']

def all_defense():
    return ['Rocket Launcher', 'Light Laser', 'Heavy Laser', 'Gauss Cannon',
            'Ion Cannon', 'Plasma Turret', 'Small Shield Dome', 'Large Shield Dome',
            'Anti-Ballistic Missiles', 'Interplanetary Missiles']



class Coordinates:
    """
    Class for storing coordinates as a list of integers
    """

    def __init__(self, string):
        """    
        The constructor accepts a string like [x:y:z] or "x:y:z"

        Raises a ValueError if the coordinates are not in the correct range

        Raises a TypeError if the string passed to the constructor is not a valid string
        """

        search = re.findall('\d+', string)
        if search:
            self.coordinates = [int(elem) for elem in search]
            if not 1 <= self.coordinates[0] <= 9 or not 1 <= self.coordinates[1] <= 499 or not 1 <= self.coordinates[2] <= 15:
                raise ValueError("""Incorrect value for the coordinates. Either
                                --- Galaxy is wrong: {0}
                                --- Solar system is wrong: {1}
                                --- Position is wrong: {2}""".format(*self.coordinates)
        else:
           raise TypeError('Incorrect string for initializing coordinates: "{0}"'.format(string))

    def __str__(self):
        return '[{0}:{1}:{2}]'.format(self.coordinates[0], self.coordinates[1], self.coordinates[2])


    def distance(self, coords):
        """
        Compute the distance to another coordinates, given
        by another Coordinates object

        Ref: http://ogame.wikia.com/wiki/Distance
        """

        if self.coordinates[0] != coords.get_galaxy():
            return 20000 * abs(self.coordinates[0] - coords.get_galaxy())
        elif self.coordinates[1] != coords.get_solar_system():
            return 2700 + 95 * abs(self.coordinates[1] - coords.get_solar_system())
        else:
            return 1000 + 5 * abs(self.coordinates[2] - coords.get_position())

    def get_galaxy(self, string = False):
        """
        Returns an integer if string == False
        otherwise returns a string
        """

        if string:
            return str(self.coordinates[0])
        return self.coordinates[0]

    def get_solar_system(self, string = False):
        """
        Returns an integer if string == False
        otherwise returns a string
        """

        if string:
            return str(self.coordinates[1])
        return self.coordinates[1]
    
    def get_position(self, string = False):
        """
        Returns an integer if string == False
        otherwise returns a string
        """

        if string:
            return str(self.coordinates[2])
        return self.coordinates[2]

    
    def get_probe_time(self, coordinates2, combustion):
        """
        Return the time as a float number that it takes to send a probe from the Coordinates object to
        another Coordinates object given the level of the combustion drive
        """
        
        speed = (1 + 0.1 * combustion) * 1e8
        return 10 + 3500 * math.sqrt(10 * self.distance(coordinates2) / speed)



string = """  	
Resources on Cerova City [1:197:5] at 09-17 12:34:18
Metal:	14.933 	Crystal:	3.282
Deuterium:	267 	Energy:	2.324
Your espionage shows abnormalities in the atmosphere of the planet which suggests a activity within the last 59 minutes.
Fleets
Defense
Buildings
Metal Mine	17 	Crystal Mine	16
Deuterium Synthesizer	9 	Solar Plant	19
Robotics Factory	4 	Shipyard	4
Metal Storage	1 	Research Lab	3
Research
Espionage Technology	2 	Computer Technology	4
Armour Technology	4 	Energy Technology	3
Combustion Drive	3 	Impulse Drive	3
Laser Technology	3
Chance of counter-espionage:0%"""




class Base:
    """
    Base class for the Resources, Fleet, Defense and Research classes
    """

    def __init__(self, report):

class Resources:
    def __init__(self, report = None, res_list = None):
        if report:
            search = re.search('Metal:\s*([\d.]+)\s*Crystal:\s*([\d.]+)\s*'
            'Deuterium:\s*([\d.]+)', report)
            self.resources = [int(elem.replace('.', '')) for elem in search.groups()] 

    def get_metal(self):
        return self.resources[0]

    def get_crystal(self):
        return self.resources[1]

    def get_deuterium(self):
        return self.resources[2]

    def get_total(self):
        return sum(self.resources)

    def get_max_loot(self):
        return (sum(self.resources) / 2, self.resources[0] / 2, self.resources[1] / 2, self.resources[2] / 2)

    def probes_needed(self):
        return get_max_loot(self) // 5 + 1

class Fleet:
    def __init__(self, report = None, fleet_list = None):
        if report:
            pass

class Defense:
    def __init__(self, report = None, defense_list = None):
        self.num = {}
        if report:
            for defense in all_defense():
                search = re.search(defense + '\s*(\d*)', report)
                if search:
                    self.num[defense] = int(search.group(1))
                else:
                    self.num[defense] = 0


    def __str__(self):
        return '\n'.join([defense + ': ' + str(self.num[defense]) for defense
            in all_defense() if self.num[defense] != 0])

    def has_defense(self):
        return any((True if self.num[defense] else False for defense in all_defense()))

class Buildings:
    def __init__(self, report = None, buildings_list = None):
        self.level = {}
        if report:
            for building in all_buildings():
                search = re.search(building + '\s*(\d*)', report)
                if search:
                    self.level[building] = int(search.group(1))
                else:
                    self.level[building] = 0


    def __str__(self):
        return '\n'.join([building + ': ' + str(self.level[building]) for building

            in all_buildings() if self.level[building] != 0])


class Research:
    def __init__(self, report = None, research_list = None):
        self.level = {}
        if report:
            for research in all_research():
                search = re.search(research + '\s*(\d*)', report)
                if search:
                    self.level[research] = int(search.group(1))
                else:
                    self.level[research] = 0

    def __str__(self):
        return '\n'.join([research + ': ' + str(self.level[research]) for research in
            all_research() if self.level[research] != 0])


class Report(Resources, Fleet, Defense, Buildings, Research):
    def __init__(self, report):
        Resources.__init__(self, report)
        Fleet.__init__(self, report)
        Buildings.__init__(self, report)
        Defense.__init__(self, report)
        Research.__init__(self, report)
        info = re.search('Resources on ([\w\- ]+) ([\d:[\]]+) at ([\w-]+) ([\d:]+)', report)
        self.planet_name = info.group(1)
        self.coords = Coordinates(info.group(2))
        date = info.group(3)
        date_search = re.search('(\d*)-(\d*)', date)
        self.date = date_search.group(2) + '-' + date_search.group(1)
        self.time = info.group(4)

    def __str__(self):
        return 'Report on {0} {1} at {2} on {3}'.format(self.planet_name, self.coords, self.time, self.date)

    def get_coordinates(self):
        return self.coords


a = Report(string)
print(type(a) == Resources)
print(a)

