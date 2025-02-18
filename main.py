import requests
import json
import webbrowser
import spotipy
import sys, os, time
import msvcrt

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime
#from win11toast import notify

from stations import stations

load_dotenv()

global_buffer = ""             #Stores last song that the API called (Prevents repeat songs each API call)
global_stationID = ""

auth_manager = SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('REDIRECT_URI'),
    scope='user-modify-playback-state'
)

timeout = os.getenv('TIMEOUT')
sp = spotipy.Spotify(auth_manager=auth_manager)

def getSongLink():
    global global_stationID, global_buffer
    url = "https://xmplaylist.com/api/station/" + global_stationID

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    
        #Validates that there is a playable song
        if (data and 'results' in data and data['results'] and 'spotify' in data['results'][0] and 'track' in data['results'][0]):
        
            spotify_uri = {
                'URI': "spotify:track:" + data['results'][0]['spotify']['id'],
                'Title': data['results'][0]['track']['title'],
                'Artist': data['results'][0]['track']['artists'][0],
                'Image': data['results'][0]['spotify']['albumImageLarge']
            }
        else:
            return None
        
    except (KeyError, IndexError, TypeError) as e:
        print("Station is Unplayable at the Moment, Enter a Different Station")
        changeStation()
        return None

    #Ensures that the song given by the API is a new song, not the previous
    if spotify_uri['URI'] and spotify_uri['URI'] != global_buffer:
        sp.add_to_queue(spotify_uri['URI'])
        global_buffer = spotify_uri['URI']
        icon = {
            'src': spotify_uri['Image'],
            'placement': 'appLogoOverride'
        }

        #Prints the song added to the queue and sends a notification
        print(f"\nAdded {spotify_uri['Title']} by {spotify_uri['Artist']} to queue.")
        #notify('xmReader: Up Next!', f"{spotify_uri['Title']} by {spotify_uri['Artist']}", icon=spotify_uri['Image'])
        
    return spotify_uri

def main():
    global global_buffer, global_stationID
    start_time = datetime.now()

    welcomeMessage = r"""
 ___  ___ ___      ___  _______   _______      __      ________   _______  _______   
|"  \/"  |"  \    /"  |/"      \ /"     "|    /""\    |"      "\ /"     "|/"      \  
 \   \  / \   \  //   |:        (: ______)   /    \   (.  ___  :|: ______):        | 
  \\  \/  /\\  \/.    |_____/   )\/    |    /' /\  \  |: \   ) ||\/    | |_____/   ) 
  /\.  \ |: \.        |//      / // ___)_  //  __'  \ (| (___\ ||// ___)_ //      /  
 /  \   \|.  \    /:  |:  __   \(:      "|/   /  \\  \|:       :|:      "|:  __   \  
|___/\___|___|\__/|___|__|  \___)\_______|___/    \___|________/ \_______)__|  \___) """
    
    print(welcomeMessage)
    
    print("\nThank you for using xmReader!\nTo Exit or Stop, Press 'q'\nTo Change Station, Press 'c'")
    changeStation()
    
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode().lower()
            if key == 'q': 
                print("Closing!")
                sys.exit()
            if key == 'c':
                changeStation()
        getSongLink()
        # Check our timer
        if timeout:
            # Compare our current time against our start time
            current_time = datetime.now()
            # Calculate the difference
            difference = current_time - start_time
            # Get the difference in seconds
            difference_in_seconds = difference.total_seconds()
            # Kill the app if we exceed our timeout
            if difference_in_seconds > timeout:
                print("xmSync closed due to the timeout configuration")
                sys.exit()

def changeStation():
    global global_stationID
    print("Please Enter The Station Name Below!")
    while True:
        station = input()

        if station in stations:
            global_stationID = stations[station]
            break
        else:
            print("Invalid Station, Try Again or Refer to stations.py")
    

main()