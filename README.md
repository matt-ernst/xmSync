# Description
### As a seemless background process, xmReader polls the xmPlaylist API to find what your favorite stations are listening to, adding the current playing song to your Spotify queue, allowing semi-synchronized SiriusXM streaming.

# Pre-Requisites
* A Spotify account (Free or Premium)
* Windows 11
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
```
SPOTIFY_CLIENT_ID=insertYourSpotifyClientIDHere
SPOTIFY_CLIENT_SECRET=insertYourSpotifyClientSecretKeyHere
REDIRECT_URI=http://localhost:8888/callback
```

# 3.) Select Your Desired Station in `stations.py`
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

### If you wanted the John Mayer station, modify the active_station assignment like the following...
```
active_station = stations["johnmayer"]
```

# 4.) Install Dependencies
### Dependencies are already packaged in the `requirements.txt`, run the following command to resolve them.
* Copy the path to `requirements.txt`
* Run the command `pip install -r "path/to/requirements.txt`

# 5.) Listen Along!
* Open Spotify
* Run `main.py`
* For first time listeners, it should ask you to authenticate via Oauth in a browser prompt.
