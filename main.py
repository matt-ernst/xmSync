import requests
import json
import webbrowser
import time
import spotipy
import os
import sys
import time
import msvcrt

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from win11toast import notify

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
    global global_stationID
    url = "https://xmplaylist.com/api/station/" + global_stationID

    try:
        time.sleep(1)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(response)
        
        spotify_uri = {
            'URI': "spotify:track:" + data['results'][0]['spotify']['id'],
            'Title': data['results'][0]['track']['title'],
            'Artist': data['results'][0]['track']['artists'][0],
            'Image': data['results'][0]['spotify']['albumImageLarge']
        }
        if spotify_uri['URI'] and spotify_uri['URI'] != global_buffer:
            sp.add_to_queue(spotify_uri['URI'])
            global_buffer = spotify_uri['URI']
            icon = {
                'src': spotify_uri['Image'],
                'placement': 'appLogoOverride'
            }
            print(f"Added {spotify_uri['Title']} by {spotify_uri['Artist']} to queue.")
        return spotify_uri

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    global global_buffer, global_stationID 
    print("Enter Desired Station: ")
    station = input()

    if station in stations:
        global_stationID = stations[station]
    else:
        print("Invalid Station")
        sys.exit()

    print("Press 'q' to quit")
    
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode().lower()
            if key == 'q':  #Press 'q' to quit
                sys.exit()
    
        getSongLink()

main()