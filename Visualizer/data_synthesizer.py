import sys
import os

sys.path.append(os.path.abspath('../TrackList'))

from tracklists_data import *
from spotify_metrics import *

def get_data(url):
    tl = trackList(url)
    tl_df = tl.output_table()
    
    tl_ids = tl_df["id"].dropna().unique()
    
    tl_media = {track_id: get_external_media(track_id) for track_id in tl_ids}
    tl_media = {track_id: media for track_id, media in tl_media.items() if media is not None}
    tl_media_df = pd.DataFrame.from_dict(tl_media, orient = "index")
    
    tl_df = pd.merge(tl_df, tl_media_df, how = "outer", left_on = "id", right_index = True).sort_index()
    
    tl_spotify_ids = tl_df["spotify0"].dropna().unique()
    tl_spotify_metrics = pd.concat([get_spotify_song_metrics(spotify_id) for spotify_id in tl_spotify_ids])
    
    tl_df = tl_df.reset_index().merge(tl_spotify_metrics, how = "outer", left_on = "spotify0", right_on = "id").set_index("index").sort_index()
    
    return(tl_df)
