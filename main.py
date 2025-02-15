import requests
import json
import webbrowser
import time
import spotipy
import os
import sys
#import msvcrt

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
#from win11toast import notify

from stations import stations
from stations import active_station

load_dotenv()

stationID = active_station     #Set your active station here (Can be modified in stations.py)
buffer = ""                    #Stores last song that the API called (Prevents repeat songs each API call)

auth_manager = SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('REDIRECT_URI'),
    scope='user-modify-playback-state'
)

sp = spotipy.Spotify(auth_manager=auth_manager)

def getSongLink():
    url = "https://xmplaylist.com/api/station/" + stationID
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        #Parses the return string for the Spotify URI.
        songURI = "spotify:track:" + data['results'][0]['spotify']['id']
        songTitle = data['results'][0]['track']['title']
        songArtist = data['results'][0]['track']['artists'][0]
        songImage = data['results'][0]['spotify']['albumImageLarge']

        songData = {
            'URI': songURI,
            'Title': songTitle,
            'Artist': songArtist,
            'Image': songImage
        }

        return songData

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    global buffer

    #Type Prompt for Channel (Refer to stations.py)
    print("Enter Desired Station: ")

    #Wait for keyboard input for station selection, as a string
    station = input()

    if station in stations:
        stationID = stations[station]
    else:
        print("Invalid Station")
        sys.exit()

    print("Press 'q' to quit")
    
    while True:
        #Checks keyboard input
        #if msvcrt.kbhit():
        #    key = msvcrt.getch().decode().lower()
        #    if key == 'q':  #Press 'q' to quit
        #        sys.exit()
    
        spotify_uri = getSongLink()
        artist = spotify_uri['Artist']
        song = spotify_uri['Title']
        album = spotify_uri['Image']
        spotify_uri = spotify_uri['URI']
        
        #If the song is new, add to queue, and send notif
        if spotify_uri and spotify_uri != buffer: # 
            sp.add_to_queue(spotify_uri)
            buffer = spotify_uri

            icon = {
                'src': album,
                'placement': 'appLogoOverride'
            }

            #notify('xmReader: Up Next!', f'{song} by {artist}', icon=icon)
            print(f"Added {song} by {artist} to queue.")

main()