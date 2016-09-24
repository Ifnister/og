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
29.965 	28.161 	16.418 	-10/2.049

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
	09-23 20:13:37 	Fleet command 	Reaching a planet
	Your fleet arrived at the planet [[1:199:5]] and delivered its goods:
Metal:25.000 Crystal:0 Deuterium:0.
	09-23 19:49:20 	Fleet command 	Return of a fleet
	One of your fleets (Espionage Probe: 166 ) returns from [1:197:5] to Planet [1:199:10] . The fleet is delivering 367 Metal, 367 Crystal and 95 Deuterium.
	09-23 19:48:19 	Fleet Command 	Battle Report (0,166) [1:197:5] (V:0,A:0)
	09-23 18:18:58 	Onpu [1:154:9] 	Re:no subjectanswer
	Ola presiosoh
	09-23 17:28:52 	Fleet command 	Reaching a planet
	Your fleet arrived at the planet [[1:199:5]] and delivered its goods:
Metal:35.000 Crystal:0 Deuterium:0.
	09-23 16:54:02 	Space monitoring 	Resource delivery by foreign fleet
	A foreign fleet from SyRaToR is delivering resources Planet [[1:199:10]]:
Metal:0 Crystal:0 Deuterium:30.000
Previously you had: Metal:55.021 Crystal:55.693 Deuterium:5.034
Now you have: Metal:55.021 Crystal:55.693 Deuterium:35.034
	09-23 15:54:46 	SyRaToR [1:199:11] 	Re:no subjectanswer
	Hi, ill can send you up to 60k Deut...
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
        print(mes)
        input()
        auxmes = Message(mes)
        if auxmes.is_fleet_return:
            ls.append(auxmes)
    return ls

print(message_parser(test))
