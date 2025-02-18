# Description
### xmSync syncs your 'Now Playing' on Spotify with any SiriusXM station of your choice using Spotipy, Spotify, and the xmPlaylist API!

# Features
* Supports any Music Playing SiriusXM Stations
* Desktop Notifications with Album Covers
  
# Pre-Requisites
* A Spotify account (Premium required for API access)
* Python
* Spotify Desktop
* Spotify API Keys
  
# 1.) Obtain Spotify API Keys
* Visit the [Spotify Developer Dashboard](https://developer.spotify.com)
* Log in with your Spotify account
* Create a new application
* Note down your Client ID and Client Secret
* `http://localhost:8888/callback` will be your Redirect URI
  
# 2.) Supply Credentials in Environment File
* Create a .env File in the Script Directory
* Copy and paste your Client ID and Client Secret
* Use the same Redirect URI
* The Timeout Value is the Amount of Time the Program Will Run Before Killing its Process
```
SPOTIFY_CLIENT_ID=insertYourSpotifyClientIDHere
SPOTIFY_CLIENT_SECRET=insertYourSpotifyClientSecretKeyHere
REDIRECT_URI=http://localhost:8888/callback
TIMEOUT=minutes
```

# 3.) Install Dependencies
### Dependencies are already packaged in the `requirements.txt`, run the following command to resolve them.
* Copy the path to `requirements.txt`
* Run the command `pip install -r "path/to/requirements.txt`

# 4.) View the Station List
### Stations are listed in the following format...
```
"johnmayer": "lifewithjohnmayer",     # Your personal soundtrack
"beatles": "thebeatleschannel",       # The Fab Four, 24/8
"bobmarley": "bobmarleystuffgong",    # Bob's music/family recordings
"springsteen": "estreetradio",        # Bruce Springsteen, 24/7
"dave": "davematthewsbandradio",      # 24/7 Dave Matthews Band
"petty": "tompettyradio",             # Music from rock icon Tom Petty
"u2": "u2xradio",                     # The whole world of U2
```

# 5.) Listen Along!
* Run `main.py`, have Spotify open already.
* For first time listeners, it should ask you to authenticate via Oauth in a browser prompt.
* Punch in the station ID listed in `station.py`
* Now, anytime a song change is noted from the xmPlaylist API, the song will be added to your Spotify queue!
