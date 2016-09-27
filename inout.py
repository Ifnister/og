from autopilot.input import Mouse, Keyboard
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

def do(ls):
    for elem in ls:
        if elem == 'Enter':
            keyboard.press_and_release('Enter')
        else:
            keyboard.type(elem, delay = 0)

def get_text():
    """
    Get clipboard text
    """
    keyboard.press_and_release('Ctrl+a', delay = 0)
    keyboard.press_and_release('Ctrl+c', delay = 0)
    return top.clipboard_get()


def tab_to(string, enter = True):
    keyboard.type('\t' * _TABS[string], delay = 0)
    if enter:
        keyboard.press_and_release('Enter', delay = 0)

def tab_positions(num, enter = True):
    keyboard.type('\t' * num, delay = 0)
    if enter:
        keyboard.press_and_release('Enter', delay = 0)


