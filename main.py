import requests
import json
import webbrowser
import spotipy
import sys, os, time
import msvcrt

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
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

sp = spotipy.Spotify(auth_manager=auth_manager)

def getSongLink():
    global global_stationID, global_buffer
    url = "https://xmplaylist.com/api/station/" + global_stationID

    try:
        #API Request
        time.sleep(5)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        spotify_uri = {
            'URI': "spotify:track:" + data['results'][0]['spotify']['id'],
            'Title': data['results'][0]['track']['title'],
            'Artist': data['results'][0]['track']['artists'][0],
            'Image': data['results'][0]['spotify']['albumImageLarge']
        }

        #Ensures that the song given by the API is a new song, not the previous
        if spotify_uri['URI'] and spotify_uri['URI'] != global_buffer:
            sp.add_to_queue(spotify_uri['URI'])
            global_buffer = spotify_uri['URI']
            icon = {
                'src': spotify_uri['Image'],
                'placement': 'appLogoOverride'
            }

            #Prints the song added to the queue and sends a notification
            print(f"Added {spotify_uri['Title']} by {spotify_uri['Artist']} to queue.")
            #notify('xmReader: Up Next!', f"{spotify_uri['Title']} by {spotify_uri['Artist']}", icon=spotify_uri['Image'])
        
        return spotify_uri

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    global global_buffer, global_stationID

    welcomeMessage = r"""
 ___  ___ ___      ___  _______   _______      __      ________   _______  _______   
|"  \/"  |"  \    /"  |/"      \ /"     "|    /""\    |"      "\ /"     "|/"      \  
 \   \  / \   \  //   |:        (: ______)   /    \   (.  ___  :|: ______):        | 
  \\  \/  /\\  \/.    |_____/   )\/    |    /' /\  \  |: \   ) ||\/    | |_____/   ) 
  /\.  \ |: \.        |//      / // ___)_  //  __'  \ (| (___\ ||// ___)_ //      /  
 /  \   \|.  \    /:  |:  __   \(:      "|/   /  \\  \|:       :|:      "|:  __   \  
|___/\___|___|\__/|___|__|  \___)\_______|___/    \___|________/ \_______)__|  \___) """
    
    print(welcomeMessage)
    
    print("\nThank you for using xmReader! To Exit or Stop, Press 'q' \nPlease Enter The Station Name Below!")
    while True:
        station = input()

        if station in stations:
            global_stationID = stations[station]
            break
        else:
            print("Invalid Station, Try Again or Refer to 'stations.py'!")
    
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode().lower()
            if key == 'q': 
                print("Closing!")
                sys.exit()
    
        getSongLink()



main()