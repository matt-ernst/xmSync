import requests
import json
import webbrowser
import spotipy
import sys, os, time
import msvcrt

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime

from stations import stations


global_buffer = ""             #Stores last song that the API called (Prevents repeat songs each API call)
global_stationID = ""          #Stores the station ID that the user wants to listen to
global_sp = None               #Spotify API Object

def getSongLink():
    global global_stationID, global_buffer, global_sp

    try:
        url = "https://xmplaylist.com/api/station/" + global_stationID
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    
        #Validates That There is a Playable Song
        if (data and 'results' in data and data['results'] and 'spotify' in data['results'][0] and 'track' in data['results'][0]):
            spotify_uri = {
                'URI': "spotify:track:" + data['results'][0]['spotify']['id'],
                'Title': data['results'][0]['track']['title'],
                'Artist': data['results'][0]['track']['artists'][0],
                'Image': data['results'][0]['spotify']['albumImageLarge']
            }
        
        #No Playable Song, Returns None, Exception is Triggered.
        else:
            return None
        
    except (KeyError, IndexError, TypeError) as e:
        print("Station is Unplayable at the Moment, Enter a Different Station")
        changeStation()
        return None

    #Compares the most recent song xmPlaylist returned with what is currently in queue. If they are different, the song is added to the queue
    if spotify_uri['URI'] and spotify_uri['URI'] != global_buffer:
        try:
            global_sp.add_to_queue(spotify_uri['URI'])
            global_buffer = spotify_uri['URI']
            
            icon = {
                'src': spotify_uri['Image'],
                'placement': 'appLogoOverride'
            }

            print(f"Added {spotify_uri['Title']} by {spotify_uri['Artist']} to queue.")
            #notify('xmSync: Up Next!', f"{spotify_uri['Title']} by {spotify_uri['Artist']}", icon=spotify_uri['Image'])
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 404 and 'No active device' in str(e):
                print("No active device found. Please start playing music on a device and try again.")
                changeStation()
            else:
                print(f"An error occurred: {e}")
        
    return spotify_uri

def main():
    global global_buffer, global_stationID
    
    #Initializes Spotify OAuth first, if it fails, the program will exit.
    oauthConnection()

    timeout = int(os.getenv('TIMEOUT'))
    start_time = datetime.now()
    
    welcomeMessage = r""""                                                                                               
___   ___ .___  ___.      _______.____    ____ .__   __.   ______ 
\  \ /  / |   \/   |     /       |\   \  /   / |  \ |  |  /      |
 \  V  /  |  \  /  |    |   (----` \   \/   /  |   \|  | |  ,----'
  >   <   |  |\/|  |     \   \      \_    _/   |  . `  | |  |     
 /  .  \  |  |  |  | .----)   |       |  |     |  |\   | |  `----.
/__/ \__\ |__|  |__| |_______/        |__|     |__| \__|  \______|
                                                                """
    
    print(welcomeMessage)
    
    print("\nThank you for using xmSync!\nTo Exit or Stop, Press 'q'\nTo Change Station, Press 'c'")
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

        #Check if Timeout variable is set
        if timeout and timeout != 0:
            #Compare our current time against our start time
            current_time = datetime.now()

            #Calculate difference in seconds
            time_difference = (current_time - start_time).total_seconds()

            # Kill the app if we exceed our timeout
            if time_difference > timeout:
                print("xmSync Closed due to Timeout Configuration")
                sys.exit()

def changeStation():
    global global_stationID

    print("Please Enter The Station Name Below!")
    while True:
        station = input()

        if station in stations:
            global_stationID = stations[station]
            print("\n")
            break
        else:
            print("Invalid Station, Try Again or Refer to stations.py")
    
def oauthConnection():
    global global_sp

    try:
        load_dotenv()
        auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URI'),
        scope='user-modify-playback-state'
    )
    except Exception as e:
        print("Error initializing Spotify OAuth, Check That .env is Properly Completed" )
        sys.exit(1)

    global_sp = spotipy.Spotify(auth_manager=auth_manager)
main()