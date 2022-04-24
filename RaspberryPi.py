# lsusb to check device name
# dmesg | grep "tty" to find port name
import serial
import time
import spotipy
import json
import webbrowser


def parseOutput(output):
    print(output)



if __name__ == '__main__':

    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 9600, timeout=.5) as arduino:
        time.sleep(0.1)  # wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    output = ""
                    time.sleep(0.1) #wait for arduino to answer
                    while arduino.inWaiting() == 0:
                        pass
                    if arduino.inWaiting() > 0:
                        #read output from arduino
                        answer = arduino.readline()

                        output = answer.decode("Ascii")
                        # print(output)
                        #Parse output from arduino
                        parseOutput(output)
                        arduino.flushInput()  # remove data after reading
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")