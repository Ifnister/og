from autopilot.input import Mouse, Keyboard 
import re
import time
import tkinter as tk

mouse = Mouse.create()
keyboard = Keyboard.create()
top = tk.Tk()
top.withdraw()

_TABS = {'Overview' : 3, 'Buildings' : 4, 'Resources' : 5, 'Research' : 6,
        'Shipyard' : 7, 'Fleet' : 8, 'Technology' : 9, 'Galaxy' : 10, 'Defense' : 11,
        'Alliance' : 12, 'Statistics' : 13, 'Search' : 14, 'Messages' : 15,
        'Notes' : 16, 'Buddylist' : 17, 'Options' : 18, 'Logout' : 19, 'Rules' : 20,
        'Legal Notice' : 21, 'ALL' : 22}

_DEFAULT_DELAY = 0.005

def do(ls, delay = _DEFAULT_DELAY):
    for elem in ls:
        if elem == 'Enter':
            keyboard.press_and_release('Enter')
        else:
            keyboard.type(elem, delay = delay)

def press(key, delay = _DEFAULT_DELAY):
    keyboard.press_and_release(key, delay = delay)

def check_clipboard(clipboard, section = 'Overview'):
    _length_error = 'Lenght too low to be a clipboard of the section {0}. Length passed was: {1}'.format(
            section, len(clipboard))
    if section == 'Overview':
        if len(clipboard) < 300:
            print(_length_error)
            return False
        search = re.search('Server time\s*\w* \w* \w* (\d+:\d\d:\d\d)', clipboard)
        if not search:
            print('Date and time not found in the clipboard:\n{0}'.format(clipboard))
            return False
        else:
            timenow = time.ctime()
            timenow = [int(elem) for elem in re.search('(\d\d:\d\d:\d\d)', timenow).group(1).split(':')]
            ogtime = [int(elem) for elem in search.group(1).split(':')]
            t1 = sum([60 ** (2 - i) * timenow[i] for i in range(3)])
            t2 = sum([60 ** (2 - i) * ogtime[i] for i in range(3)])
            print(timenow, ogtime, t1, t2)
            print(min(abs(t1 - t2), abs(min(t1, t2) + 86400 - max(t1, t2))))
            if min(abs(t1 - t2), abs(min(t1, t2) + 86400 - max(t1, t2))) > 3:
                print("""Local time and ogame time difference is greater than 3 seconds:
                Ogame time: {0}
                Local time: {1}""".format(ogtime, timenow))
                return False
    elif section == 'Fleet':
        if clipboard.find('Fleets (max. ') == -1 or clipboard.find(
                'Please select your ships for this mission:') == -1:
            return False
    elif section == 'Fleet2':
        if clipboard.find('Choose Target') == -1 or clipboard.find(
                'Duration (one way)') == -1:
            return False
    elif section == 'Fleet3':
        if clipboard.find('Cargo Options') == -1 or clipboard.find(
                'all resources') == -1:
            return False
    return True

def get_text():
    """
    Get clipboard text
    """
    keyboard.press_and_release('Ctrl+a', delay = 0)
    time.sleep(0.05)
    keyboard.press_and_release('Ctrl+c', delay = 0)
    time.sleep(0.05)
    return top.clipboard_get()


def tab_to(string, enter = True):
    keyboard.type('\t' * _TABS[string], delay = 0)
    if enter:
        keyboard.press_and_release('Enter', delay = 0)
    time.sleep(0.1)

def tab_positions(num, enter = True):
    keyboard.type('\t' * num, delay = 0)
    if enter:
        keyboard.press_and_release('Enter', delay = 0)



