# lsusb to check device name
# dmesg | grep "tty" to find port name
import serial
import time
import spotipy
import json
import webbrowser

global clientID
global clientSecret
global spotifyUserName
global redirectURL

clientID = "b6dc4115b3e54349b7d02bbf3f865f85"
clientSecret = "31d4d345bc114da39414613c1ce45a38"
spotifyUserName = "noah_allen24"
redirectURL = "http://google.com/"



def parseOutput(output):
    print(output)



if __name__ == '__main__':
    oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    print(json.dumps(user,sort_keys=True, indent=4))
    print("Welcome, "+ user['display_name'])
    
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