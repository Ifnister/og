import re
import math



_RESOURCES = ['Metal', 'Crystal', 'Deuterium', 'Energy']

_BUILDINGS =  ['Metal Mine', 'Crystal Mine', 'Deuterium Synthesizer',
        'Solar Plant', 'Fusion Reactor', 'Robotics Factory',
        'Nanite Factory', 'Shipyard', 'Metal Storage', 'Crystal Storage',
        'Deuterium Tank', 'Research Lab', 'Terraformer', 'Missile Silo',
        'Lunar Base', 'Sensor Phalanx', 'Jump Gate']

_SHIPS = ['Small Cargo', 'Large Cargo', 'Light Fighter', 'Heavy Fighter',
        'Cruiser', 'Battleship', 'Colony Ship', 'Recycler', 'Espionage Probe',
        'Bomber', 'Solar Satellite', 'Destroyer', 'Deathstar']

_DEFENSE = ['Rocket Launcher', 'Light Laser', 'Heavy Laser', 'Gauss Cannon',
            'Ion Cannon', 'Plasma Turret', 'Small Shield Dome', 'Large Shield Dome',
            'Anti-Ballistic Missiles', 'Interplanetary Missiles']

_RESEARCH = ['Espionage Technology', 'Computer Technology', 'Weapons Techonology',
            'Shielding Techonology', 'Armour Technology', 'Energy Technology',
            'Hyperspace Technology', 'Combustion Drive', 'Impulse Drive',
            'Hyperspace Drive', 'Laser Technology', 'Ion Technology']


def all_ships_properties():
    """
    Return all of the ship's properties as a dictionary
    """
    pass


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
                                --- Position is wrong: {2}""".format(*self.coordinates))
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



def _constructor(report, ls):
    dic = {}
    for elem in ls:
        search = re.search(elem + ':?\s*([\d.]+)', report)
        if search:
            num = int(search.group(1).replace('.', '')) 
            dic[elem] = num
        else:
            dic[elem] = 0
    return dic



_LINE_LENGTH = 60
_TEXT_NUMBER_OFFSET = 22


def _report_str(dic, ls):
    auxls = []
    subls = []
    counter = 0
    for elem in ls:
        assert _TEXT_NUMBER_OFFSET - len(elem) + 1 >= 0
        subls.append(elem + ' ' * (_TEXT_NUMBER_OFFSET - len(elem) + 1) + str(dic[elem]) + ' ' * (_LINE_LENGTH // 2 - _TEXT_NUMBER_OFFSET - len(str(dic[elem]))))
        counter += 1
        if not counter % 2:
            auxls.append(''.join(subls))
            subls = []
    return '\n'.join(auxls)

        
        
        

    
    

class Resources:
    def __init__(self, report = None):
        if report:
            self.res = _constructor(report, _RESOURCES)

    def get_metal(self):
        return self.res['Metal']

    def get_crystal(self):
        return self.res['Crystal']

    def get_deuterium(self):
        return self.res['Deuterium']

    def get_total(self):
        return sum(self.res.values())

    def get_max_loot(self):
        return (sum(self.res.values()) / 2, self.res[_RESOURCES[0]] / 2,
                self.res[_RESOURCES[1]] / 2, self.res[_RESOURCES[2]] / 2)
  
    def get_probes_needed(self):
        return get_max_loot(self) // 5 + 1

    def __str__(self):
        return _report_str(self.res, _RESOURCES)
        return 'Metal:\t\t{0}\t\tCrystal:\t{1}\nDeuterium:\t{2}\t\tEnergy:\t\t{3}'\
                .format(self.res['Metal'], self.res['Crystal'], self.res['Deuterium'], self.res['Energy'])
        

class Fleet:
    def __init__(self, report = None):
        if report:
            if re.search('Fleets', report):
                self.in_report = True
                self.fleet = _constructor(report, _SHIPS)
            else:
                self.in_report = False

    def __str__(self):
        return _report_str(self.fleet, _SHIPS)
    
    def is_in_report(self):
        try:
            return self.in_report
        except NameError:
            raise NameError('Checking if \'Fleets\' appears in the report with no report submitted') 


class Defense:
    def __init__(self, report = None):
        if report:
            if re.search('Defense', report):
                self.in_report = True
                self.defense = _constructor(report, _DEFENSE)
            else:
                self.in_report = False

    def is_in_report(self):
        try:
            return self.in_report
        except NameError:
            raise NameError('Checking if \'Defense\' appears in the report with no report submitted') 

    def __str__(self):
        return _report_str(self.defense, _DEFENSE)
        return '\n'.join([defense + ': ' + str(self.defense[defense]) for defense
            in _DEFENSE if self.defense[defense] != 0])

    def has_defense(self):
        return any((True if self.defense[defense] else False for defense in _DEFENSE()))

class Buildings:
    def __init__(self, report = None):
        if report:
            if re.search('Buildings', report):
                self.in_report = True
                self.buildings = _constructor(report, _BUILDINGS)
    def is_in_report(self):
        try:
            return self.in_report
        except NameError:
            raise NameError('Checking if \'Buildings\' appears in the report with no report submitted') 

    def __str__(self):
        return _report_str(self.buildings, _BUILDINGS)
        return '\n'.join([building + ': ' + str(self.buildings[building]) for building
            in _BUILDINGS if self.buildings[building] != 0])


class Research:
    def __init__(self, report = None):
        if report:
            if re.search('Research', report):
                self.in_report = True
                self.research = _constructor(report, _RESEARCH)
            else:
                self.in_report = False

    def is_in_report(self):
        try:
            return self.in_report
        except NameError:
            raise NameError('Checking if \'Research\' appears in the report with no report submitted') 

    def __str__(self):
        return _report_str(self.research, _RESEARCH)
        return '\n'.join([research + ': ' + str(self.research[research]) for research in
            _RESEARCH if self.research[research] != 0])


_CORE_CLASSES = [Resources, Fleet, Defense, Buildings, Research]

class Report(Resources, Fleet, Defense, Buildings, Research):
    def __init__(self, report):
        for elem in _CORE_CLASSES:
            elem.__init__(self, report)
        info = re.search('Resources on ([\w\- ]+) ([\d:[\]]+) at ([\w-]+) ([\d:]+)', report)
        self.planet_name = info.group(1)
        self.coords = Coordinates(info.group(2))
        date = info.group(3)
        date_search = re.search('(\d*)-(\d*)', date)
        self.date = date_search.group(2) + '-' + date_search.group(1)
        self.time = info.group(4)

    def __str__(self):
        ls = ['Report on {0} {1} at {2} on {3}\n\n'.format(self.planet_name, self.coords, self.time, self.date) +\
            Resources.__str__(self)]
        for elem in _CORE_CLASSES:
            if elem == Resources:
                continue
            if elem.is_in_report(self):
                ls.append(elem.__str__(self))
        return '\n\n'.join(ls)
                

    def get_coordinates(self):
        return self.coords



