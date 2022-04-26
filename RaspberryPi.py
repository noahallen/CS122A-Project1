# lsusb to check device name
# dmesg | grep "tty" to find port name

import serial
import time
import spotipy
import json
import webbrowser
from pynput.keyboard import Key, Controller 
from pynput.mouse import Button, Controller

#Define global variables
global clientID
global clientSecret
global spotifyUserName
global redirectURI
global songIDHashTable
global mouse
global keyboard


keyboard = Controller()
mouse = Controller()

#Env variables/secrets
clientID = "b6dc4115b3e54349b7d02bbf3f865f85"
clientSecret = "31d4d345bc114da39414613c1ce45a38"
spotifyUserName = "noah_allen24"
redirectURI = "http://google.com/"

#Hash table storing the different song/id combinations I want to include
songIDHashTable = {"8713525193": "https://open.spotify.com/track/11bD1JtSjlIgKgZG2134DZ?si=789cb325d2c146e4"}

def parseOutput(output):
    print(output)
    if(output in songIDHashTable.keys()):
        return songIDHashTable[output]
    else:
        return ""

#Tells the raspberry pi to move the mouse to the window close button and press it to close a window
def closeWindow():
    mouse.position = (788, 50)
    mouse.press(Button.left)
    mouse.release(Button.left)

#Tells the raspberry pi to move the mouse to the spotify play/pause button and press it to play/pause a song
def playPause():
    mouse.position = (296, 584)
    mouse.press(Button.left)
    mouse.release(Button.left)


if __name__ == '__main__':

    #Instantiate the spotify objects
    oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    print(json.dumps(user,sort_keys=True, indent=4))
    print("Welcome, "+ user['display_name'])

    #Connect with serial output from the arduino
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 9600, timeout=.5) as arduino:
        time.sleep(0.1)  # wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                songOpened = False
                # Loop through until arduino sends information through serial port
                while True:
                    output = ""
                    time.sleep(0.1) #wait for arduino to answer
                    while arduino.inWaiting() == 0:
                        pass
                    if arduino.inWaiting() > 0:
                        # Read output from arduino
                        answer = arduino.readline()

                        output = answer.decode("Ascii")
                        # print(output)
                        # Parse output from arduino
                        songLink = parseOutput(output)
                        if(songLink == ""):
                            print("Card not recognized")
                        else:
                            # Checks the flag if a song has been opened yet in order to check if a window needs to be closed first
                            if(songOpened):
                                playPause()
                                time.sleep(.5)
                                closeWindow()
                            
                            # Opens spotify song in a new browser, close blank tab, and press play once loaded
                            webbrowser.open(songLink, new=0)
                            time.sleep(5)
                            closeWindow()
                            time.sleep(2)
                            playPause()
                            songOpened = True
                        arduino.flushInput()  # remove data after reading
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")