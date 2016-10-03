import core as og
import actions as act
import messages as msg
import time


objectives = [og.Coordinates("1:202:10"), og.Coordinates("1:196:8"), og.Coordinates("1:195:5")]

while True:
    duration, consumption = act.send_ships(['Espionage Probe'], ['max'], objectives[0])
    current_time = time.monotonic()
    clipboard = act.get_messages()
    message = msg.message_parser(clipboard)
    if sum(message.loot()[0]) < 5 * message.loot()[2] - 5:
        objectives.append(objectives.pop(0))
    time.sleep(duration * 2 + 3 - time.monotonic() + current_time)
    
