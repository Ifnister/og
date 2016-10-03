import core as og
import re

_ESPIONAGE_REPORT = 'Espionage Report'
_RETURN_OF_A_FLEET = 'Return of a fleet'
_BATTLE_REPORT = 'Battle Report'
_TYPES = [_ESPIONAGE_REPORT, _RETURN_OF_A_FLEET, _BATTLE_REPORT]

class Message:
    def __init__(self, message):
        search = re.search('(\d\d)-(\d\d) ([\w:])', message)
        if search:
            self.date = search.group(2) + '-' + search.group(1)
            self.time = search.group(3)
        else:
            raise ValueError('The message introduced does not have\
                    date and/or time: {0}'.format(message))
        self.message = message

        for typ in _TYPES:
            if re.search(typ, message):
                self.type = typ
                break
            else:
                self.type = 'something else'

    def __str__(self):
        return message

    def is_fleet_command(self):
        return self.type in _TYPES

    def is_report(self):
        return self.type == _ESPIONAGE_REPORT
    def is_fleet_return(self):
        return self.type == _RETURN_OF_A_FLEET
    def is_battle_report(self):
        return self.type == _BATTLE_REPORT

    def loot(self):
        if self.type != _RETURN_OF_A_FLEET:
            raise TypeError('loot method requires the message being of type\
                    "{0}"'.format(_RETURN_OF_A_FLEET))
        pattern = 'One of your fleets \(Espionage Probe: (\d+) \) returns from \[([\d:]*)\] ' +\
                'to (\w+) \[([\d:]*)\] . The fleet is delivering (\d+) Metal, (\d+) Crystal and ' +\
                '(\d+) Deuterium.'
        search = re.search(pattern, self.message) 
        if not search:
            raise ValueError('"{0}" message does not have valid data')
        num = int(search.group(1))
        objective = og.Coordinates(search.group(2))
        main_planet = og.Coordinates(search.group(4))
        resources = [int(elem) for elem in search.groups()[4 : 7]]
        return (resources, objective, num, main_planet)

        
 
test = """

Metal 	Crystal 	Deuterium 	Energy
18.752 	7.880 	3.925 	-56/2.361

Universe 1 (v 0.77)
Overview
Buildings
Resources
Research
Shipyard
Fleet
Technology
Galaxy
Defense
Alliance
Statistics
Search
Messages
Notes
Buddylist
Options
Logout
Rules
Legal Notice
^
Messages
Action 	Date 	From 	Subject
	10-03 07:41:09 	Fleet command 	Return of a fleet
	One of your fleets (Espionage Probe: 172 ) returns from [1:202:10] to Planet [1:199:10] . The fleet is delivering 422 Metal, 422 Crystal and 15 Deuterium.
	10-03 07:40:07 	Fleet Command 	Battle Report (0,172) [1:202:10] (V:0,A:0)
	10-03 07:38:56 	Fleet command 	Return of a fleet
	One of your fleets (Espionage Probe: 172 ) returns from [1:202:10] to Planet [1:199:10] . The fleet is delivering 420 Metal, 420 Crystal and 17 Deuterium.
	10-03 07:37:55 	Fleet Command 	Battle Report (0,172) [1:202:10] (V:0,A:0)
	10-03 07:36:51 	Fleet command 	Return of a fleet
	One of your fleets (Espionage Probe: 172 ) returns from [1:202:10] to Planet [1:199:10] . The fleet is delivering 418 Metal, 418 Crystal and 23 Deuterium.
	10-03 07:35:48 	Fleet Command 	Battle Report (0,172) [1:202:10] (V:0,A:0)
	10-03 07:13:22 	Fleet command 	Return of a fleet
	One of your fleets (Espionage Probe: 172 ) returns from [1:202:10] to Planet [1:199:10] . The fleet is delivering 286 Metal, 286 Crystal and 286 Deuterium.
	10-03 07:12:20 	Fleet Command 	Battle Report (0,172) [1:202:10] (V:0,A:0)
	10-03 06:50:42 	Fleet command 	Return of a fleet
	One of your fleets (Small Cargo: 10 ) returns from [1:366:5] to Planet [1:391:5] . ^
	10-03 06:31:47 	Fleet command 	Return of a fleet
	One of your fleets (Small Cargo: 28 Light Fighter: 6 Heavy Fighter: 4 Espionage Probe: 172 ) returns from [1:199:9] to Planet [1:199:10] . The fleet is delivering 471 Metal, 10.706 Crystal and 8.455 Deuterium.
show only partial espionage reports
Gameoperators




"""


def message_divider(string):
    indexs = []
    for line in string.split('\n'):
        search = re.search('\A.\d\d-\d\d [\w:]+', line)
        if search:
            indexs.append(string.find(search.group(0)))

    if indexs:
        last_index = string.find('\nshow only partial espionage reports')
    return [string[indexs[i] : indexs[i + 1]] for i in range(len(indexs) - 1)] +\
            [string[indexs[len(indexs) - 1] : last_index]]

def message_parser(string):
    ls = []
    for mes in message_divider(string):
        auxmes = Message(mes)
        if auxmes.is_fleet_return():
            ls.append(auxmes)
    return ls

print(message_parser(test))
