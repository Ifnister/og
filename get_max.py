from magic_numbers import *
import tkinter as tk
from autopilot.input import Mouse, Keyboard


def get_probe_max(mouse, keyboard):
    text = get_text(mouse, keyboard)
    text = text[text.find('Fleets (max') :]
    index = text.find('Please select your ships for this mission')
    part1 = text[0 : index]
    part2 = text[index :]
    print(part1, part2)
    if part1.split().count('-') > 3:
        number_of_missions = 0
    else:
        number_of_missions = part1.count('\n') - 2
    print(number_of_missions)
    probe_index = part2.find('Espionage Probe')
    if probe_index == -1:
        print("ERROR: THERE ARE NO PROBES IN THIS PLANET")
    number_of_ships = part2[0 : probe_index].count('\n')
    print(number_of_ships)
    if not number_of_missions:
        return (945, corner[1] + fleets_indicator[1] + id_and_mission +
                 (number_of_ships + 1) * ship +
                3 + number_of_missions + number_of_ships + 10)
    return (945, corner[1] + fleets_indicator[1] + id_and_mission +
            number_of_missions * fleet + number_of_ships * ship +
            2 + number_of_missions + number_of_ships + 10)


def get_text(mouse, keyboard):
    r = tk.Tk()
    r.withdraw()
    keyboard.press_and_release('Ctrl+a', delay = 0.05)
    keyboard.press_and_release('Ctrl+c', delay = 0)
    return r.clipboard_get()

#m.move(*get_probe_max(m, k))
    
