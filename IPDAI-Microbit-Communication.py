#imports
import tensorflow as tf
import numpy as np
import serial

# initialising serial communication
port = "COM3"
ser = serial.Serial()
ser.port = port
ser.baudrate = 115200

# loading model
model = tf.keras.models.load_model("COMPSCI-Project\model.h5")

# opening serial port
ser.open()

print("finished loading")

# initialising AI for predictions
#p1 is the opponent, p2 is the player
p1 = []
p2 = []
for i in range(8):
    # collect move data from serial port
    data = str(ser.readline().decode('utf-8')).strip()
    print(f"Move Retrieved: {data}")
    if len(data) == 1:
        data = int(data)
        if i % 2 == 0:
            p1.append(data)
        else:
            p2.append(data)

# dictionary containing actions
actions = {0: 1, 1: 2, 2: 0}

# main loop
while True:
    # take data[-4:] and convert to AI friendly format
    input_data = []
    input_data.extend(p2[-4:])
    input_data.extend(p1[-4:])
    input_data = np.array([input_data])
    print(f"Move Data: {input_data}")

    # make prediction
    prediction = model(input_data).numpy().tolist()
    action = actions[prediction[0].index(max(prediction[0]))]
    p2.append(action)
    print(f"Best Move for P2: {action}")
    x = False
    
    # send best move to microbit via serial
    ser.write(str(action).encode("utf-8"))

    # collect new player 2 move
    while not x:
        while True: 
            try:
                # collect move data from serial port
                data = str(ser.readline().decode('utf-8')).strip()
                data = data + "a"
                data = data[0]
                print(f"Move Retrieved: {data}")
                p1.append(int(data))
                x = True
                break
            except:
                ...
