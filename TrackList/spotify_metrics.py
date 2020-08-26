import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

SPOTIFY_SONG_METRICS = ['danceability', 
                'energy', 
                'key', 
                'loudness', 
                'mode', 
                'speechiness', 
                'acousticness', 
                'instrumentalness', 
                'liveness', 
                'valence', 
                'tempo', 
                'id', 
                'duration_ms', 
                'time_signature']

credentials = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=credentials)

'''
Takes spotify song id and returns spotify song features
If song name and artist are supplied instead of ID, attempts to search for the song
Search only returns metrics if artist name and song name are an exact match
'''
def get_spotify_song_metrics(song_id = None, song_name = None, song_artist = None):
    if song_id:
        song_features = sp.audio_features(song_id)
    elif song_name and song_artist:
        result = sp.search(q = "track:" + song_name + " artist:" + song_artist, type = "track", limit = 1)
    
        if result["tracks"]["items"]:
            result = result["tracks"]["items"][0]
            result_info = {
                "name" : result["name"],
                "artists" : [artist_info["name"] for artist_info in result["artists"]],
                "id" : result["id"]
            }

            if song_name == result_info["name"] and song_artist in result_info["artists"]:
              song_id = result_info["id"]
              song_features = sp.audio_features(song_id)
      
    try:
        song_features = song_features[0]

        song_metrics = pd.DataFrame([{metric : value for metric, value in song_features.items() if metric in SPOTIFY_SONG_METRICS}])
    
    except NameError:
        return(None)
    
    try:
        song_artist_id = sp.track(song_id)["artists"][0]["id"]
        song_genres = sp.artist(song_artist_id)["genres"]
        song_metrics["genres"] = ",".join(song_genres)
    except:
        song_metrics["genres"] = np.nan
    
    return(song_metrics)