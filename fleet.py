from core import _SHIPS
import time
import core
import inout
import re


def get_recall_num(clipboard):
    """
    Get the number of mission that can be recalled
    clipboard is the Overview clipboard
    """
    count = 0
    dic = {}
    newclip = clipboard[clipboard.find('Events') : ]
    search = re.findall('is: (\w+)', newclip)
    for mission in search:
        if mission != 'Deployment':
            count += 1
    return count

def get_ship_num(clipboard):
    newclip = clipboard[clipboard.find('Available') : ]
    ships = []
    num = []
    for ship in _SHIPS:
        search = re.search(ship + '\s*(\d*)', newclip)
        if search:
            ships.append(ship)
            num.append(int(search.group(1)))
    return [ships, num]

def get_mission_num(clipboard):
    newclip = clipboard[clipboard.find('Fleets (max') :]
    index = newclip.find('Please select your ships for this mission')
    newclip = newclip[0 : index]
    if newclip.split().count('-') > 3:
        number_of_missions = 0
    else:
        number_of_missions = newclip.count('\n') - 2
    return number_of_missions

def get_string(ships, num, available_ships, available_shipsnum):
    """
    Get the string that has to be typed to send the appropiate
    number of ships
    It is supposed that the ships to be sent are <= available ships
    """
    ls = []
    s = ""
    for ship in available_ships:
        if ship not in ships:
            s += '\t\t'
        else:
            index = ships.index(ship)
            if num[index] == 'max':
                ls.append(s)
                s = ""
                ls.append('Enter')
            else:
                s += '\t' + str(num[index])
    s += '\t\t\t'
    ls.append(s)
    return ls
                


_MED_WAIT = 1.5
    
def send_ships(ships, num, coordinates, speed = 100):
    inout.tab_to('Overview') 
    time.sleep(_MED_WAIT)
    recalls = get_recall_num(inout.get_text())
    inout.tab_to('Fleet')
    time.sleep(_MED_WAIT)
    clip = inout.get_text()
    missions = get_mission_num(clip)
    available_ships, available_shipsnum = get_ship_num(clip)
    for ship in ships:
        if ship not in available_ships:
            raise Exception
        index1 = ships.index(ship)
        index2 = available_ships.index(ship)
        if num[index1] > available_shipsnum[index2]:
            raise Exception
    inout.tab_to('ALL', False)
    print(missions, recalls)
    inout.tab_positions(2 * missions + recalls - 1, False)
    actions = get_string(ships, num, available_ships, available_shipsnum)
    print(actions)
    inout.do(actions)


send_ships(['Small Cargo', 'Light Fighter', 'Colony Ship', 'Espionage Probe'],
        [12, 1, 1, 15], 33)



