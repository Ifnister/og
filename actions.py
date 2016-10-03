from core import _SHIPS
import time
import core as og
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
    newclip = newclip[0 : newclip.find('Please select your ships for this mission')]
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
        if ship == 'Solar Satellite':
            continue
        if ship not in ships:
            s += '\t\t'
        else:
            index = ships.index(ship)
            if num[index] == 'max':
                ls.append(s)
                s = "\t\t"
                ls.append('Enter')
            else:
                s += '\t' + str(num[index]) + '\t'
    s += '\t\t'
    ls.append(s)
    ls.append('Enter')
    return ls
                

def get_duration_and_consumption(clipboard):
    search1 = re.search('Duration \(one way\)\s*\n(\d*:\d*:\d*)', clipboard)
    search2 = re.search('Deuterium consumption\s*(\d*)', clipboard)
    if search1:
        duration = sum([60 ** (2 - i) * int(search1.group(1).split(':')[i]) for i in range(3)])
    if search2:
        consumption = float(search2.group(1))
    return (duration, consumption)


_MED_WAIT = 1.5
_LOW_WAIT = 0.8
_VERYLOW_WAIT = 0.175

def get_num_of_coords(clipboard):
    """
    Get the number of times some coordinates appear in Fleet2 to be
    able to tab to the continue button
    """
    new_clip = clipboard[clipboard.find('Shortcuts') : ]
    return len(re.findall('\d:\d{3}:\d{1,2}', new_clip))

def get_num_of_downs(mission):
    """
    Get the number of times that the down arrow key has to be pressed
    in order to select the appropiate mission
    """
    if mission == 'attack':
        return 1
    elif mission == 'espionage':
        return 2


def get_messages():
    inout.tab_to('Messages')
    time.sleep(_LOW_WAIT)
    return inout.get_text()

def send_ships(ships, num, coords, speed = 100, mission = 'attack'):
    ### 
    ### Overview
    ###
    inout.tab_to('Overview') 
    time.sleep(_VERYLOW_WAIT)
    clipboard = inout.get_text()
    count = 0
    while not inout.check_clipboard(clipboard, 'Overview'):
        count += 1
        clipboard = inout.get_text()
        time.sleep(_VERYLOW_WAIT)
    print("Number of times to get out of Overview = {0}".format(count))
    recalls = get_recall_num(clipboard)
    ###
    ### Fleet
    ###
    time.sleep(_VERYLOW_WAIT)
    inout.tab_to('Fleet')
    time.sleep(_VERYLOW_WAIT)
    clipboard = inout.get_text()
    count = 0
    while not inout.check_clipboard(clipboard, 'Fleet'):
        clipboard = inout.get_text()
        time.sleep(_VERYLOW_WAIT)
        count += 1
    print("Number of times to get out of Fleet = {0}".format(count))
    missions = get_mission_num(clipboard)
    available_ships, available_shipsnum = get_ship_num(clipboard)
    for ship in ships:
        if ship not in available_ships:
            raise Exception("{0} not in {1}".format(ship, available_ships))
        index1 = ships.index(ship)
        index2 = available_ships.index(ship)
        if num[index1] == 'max':
            continue
        if num[index1] > available_shipsnum[index2]:
            raise Exception
    inout.tab_to('ALL', False)
    print(missions, recalls)
    inout.tab_positions(2 * missions + recalls, False)
    actions = get_string(ships, num, available_ships, available_shipsnum)
    print(actions)
    inout.do(actions, delay = 0.05)
    ###
    ### Fleet2
    ###
    time.sleep(_VERYLOW_WAIT)
    clipboard = inout.get_text()
    count = 0
    while not inout.check_clipboard(clipboard, 'Fleet2'):
        clipboard = inout.get_text()
        time.sleep(_VERYLOW_WAIT)
        count += 1
    print("Number of times to get out of Fleet2 = {0}".format(count))
    inout.tab_to('ALL', False)
    #Last tab is necessary, otherwise only the position in the solar system
    #will be selected
    inout.do([coords.get_galaxy(True) + '\t' + coords.get_solar_system(True) +
        '\t' + coords.get_position(True) + '\t' * 2], delay = 0.05)

    if speed != 100:
       inout.do([str(speed / 10)]) 
    clipboard = inout.get_text()
    count = 0
    while not inout.check_clipboard(clipboard, 'Fleet2'):
        clipboard = inout.get_text()
        time.sleep(_VERYLOW_WAIT)
        count += 1
    print("Number of times to get out of Fleet2(b) = {0}".format(count))
    duration, consumption = get_duration_and_consumption(clipboard)
    inout.do(['\t' * (get_num_of_coords(clipboard) + 1)])
    inout.do(['Enter'])
    time.sleep(_VERYLOW_WAIT)
    count = 0
    while not inout.check_clipboard(clipboard, 'Fleet3'):
        clipboard = inout.get_text()
        time.sleep(_VERYLOW_WAIT)
    print("Number of times to get out of Fleet3(b) = {0}".format(count))
    inout.tab_to('ALL', False)
    for k in range(get_num_of_downs(mission)):
        inout.press('Down')
    inout.do(['Enter'])
    return duration, consumption

for k in range(8):
    duration, consumption = send_ships(['Espionage Probe'], ['max'], og.Coordinates("1:202:10"))
    time.sleep(duration * 2 + 3)




