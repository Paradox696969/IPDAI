# Imports go at the top
from microbit import *
import radio

radio.on()

count = 8
while count > 0:
    display.scroll(count)
    b_a = button_a.was_pressed()
    b_b = button_b.was_pressed()

    if b_a and b_b:
        radio.send("2")
        count -= 1
    elif b_a:
        radio.send("0")
        count -= 1
    elif b_b:
        radio.send("1")
        count -= 1

while True:
    try:
        action = radio.receive()
        action = action + "a"
        action = str(action)
        display.scroll(action.replace("a", ""))
        while True:
            try:      
                b_a = button_a.was_pressed()
                b_b = button_b.was_pressed()
            
                if b_a and b_b:
                    radio.send("2")
                    break
                elif b_a:
                    radio.send("0")
                    break
                elif b_b:
                    radio.send("1")
                    break
            except:
                ...
    except Exception as e:
        ...
