# Imports go at the top
from microbit import *
import radio

radio.on()
uart.init(baudrate=115200)

count = 8
while count > 0:
    try:
        data = radio.receive()
        data = data + "a"
        print(data[0])
        count -= 1
    except:
        ...

while True:
    try:
        data = uart.readline()
        data = data + "a"
        radio.send(str(data))
        while True:
            try:
                data = radio.receive()
                data = data + "a"
                print(data[0])
                break
            except:
                ...
    except Exception as e:
        ...
