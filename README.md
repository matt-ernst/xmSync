 ___  ___ ___      ___  _______   _______      __      ________   _______  _______   
|"  \/"  |"  \    /"  |/"      \ /"     "|    /""\    |"      "\ /"     "|/"      \  
 \   \  / \   \  //   |:        (: ______)   /    \   (.  ___  :|: ______):        | 
  \\  \/  /\\  \/.    |_____/   )\/    |    /' /\  \  |: \   ) ||\/    | |_____/   ) 
  /\.  \ |: \.        |//      / // ___)_  //  __'  \ (| (___\ ||// ___)_ //      /  
 /  \   \|.  \    /:  |:  __   \(:      "|/   /  \\  \|:       :|:      "|:  __   \  
|___/\___|___|\__/|___|__|  \___)\_______|___/    \___|________/ \_______)__|  \___)

# Description
### xmReader polls the xmPlaylist API to find what your favorite SiriusXM stations are listening to, adding the current playing song to your Spotify queue, allowing semi-synchronized SiriusXM streaming.

# Features
* Supports any Music Playing SiriusXM Stations
* Desktop Notifications with Album Covers
  
# Pre-Requisites
* A Spotify account (Free or Premium)
* Windows 11
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
```
SPOTIFY_CLIENT_ID=insertYourSpotifyClientIDHere
SPOTIFY_CLIENT_SECRET=insertYourSpotifyClientSecretKeyHere
REDIRECT_URI=http://localhost:8888/callback
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
