import time
from autopilot.input import Mouse
from autopilot.input import Keyboard
import get_max
m = Mouse.create()
k = Keyboard.create()

wait_time = 123
objective = "1:196:8"
#max_position = (955, 412)
#max_position = (955, 392)
#max_position = (955, 372)
first_ok = (887, 474)
first_ok = (892, 452)
overview = (138, 214)
fleet = (149, 289)
galaxy = (161, 314)
second_ok = (897, 421)
third_ok = (884, 398)
attack_button = (737, 305)
first_field_fleet = (941, 252)

low_wait = 0.8
counter = 0
while counter < 1e9:
    counter += 1
    m.move(*fleet)
    m.click()
    time.sleep(low_wait + 0.5)
    max_position = get_max.get_probe_max(m, k)
    first_ok = (892, max_position[1] + 60)
    m.move(*max_position)
    m.click()
    m.move(*first_ok)
    m.click()
    time.sleep(low_wait)
    m.move(*first_field_fleet)
    m.click()
    k.type('\b')
    k.type(objective.split(':')[0], delay = 0.05)
    k.type('\t', delay = 0)
    k.type(objective.split(':')[1], delay = 0.05)
    k.type('\t')
    k.type(objective.split(':')[2], delay = 0.05)
    k.press_and_release('Enter', delay = 0)
    time.sleep(low_wait)
    m.move(*attack_button)
    m.click()
    k.press_and_release('Enter', delay = 0)
    time.sleep(low_wait)
    m.move(*overview)
    #m.click()
    time.sleep(wait_time)




