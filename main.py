import requests
import json
import webbrowser
import time
import spotipy
import os
import sys
import msvcrt

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from win11toast import notify

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
    
    while True:
        #Checks keyboard input for listing stations
        if msvcrt.kbhit():  # For Windows
            key = msvcrt.getch().decode().lower()
            if key == 'l':  # Press 'l' to list stations
                list_stations()
            elif key == 'h':  # Press 'h' for help
                print("\nCommands:")
                print("l - List all stations")
                print("h - Show this help menu")
                print("q - Quit program")
            elif key == 'q':  # Press 'q' to quit
                print("\nExiting program...")
                sys.exit()
    
        spotify_uri = getSongLink()
        artist = spotify_uri['Artist']
        song = spotify_uri['Title']
        album = spotify_uri['Image']
        spotify_uri = spotify_uri['URI']
        
        #If the song is new, open the Spotify URL.
        if spotify_uri and spotify_uri != buffer: 
            sp.add_to_queue(spotify_uri)
            buffer = spotify_uri

            icon = {
                'src': album,
                'placement': 'appLogoOverride'
            }

            notify('xmReader: Up Next!', f'{song} by {artist}', icon=icon)
            print(f"Added {song} by {artist} to queue.")

def list_stations():
    print("\nAvailable Stations by Category:")
    print("=" * 50)
    
    current_category = None
    
    for line in stations.keys():
        if line.startswith("# "):
            # This is a category header
            current_category = line
            print(f"\n{current_category}")
            print("-" * len(current_category))
        else:
            # This is a station entry
            station_value = stations[line]
            description = station_value.split("#")[1].strip() if "#" in station_value else ""
            print(f"{line}: {station_value}")
main()