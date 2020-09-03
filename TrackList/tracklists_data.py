import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import pandas as pd

EXTERNAL_MEDIA_LINK = "https://www.1001tracklists.com/ajax/get_medialink.php?idObject=5&idItem={track_id}&viewSource=1"

SOURCES = {
    "1": "beatport",
    "2": "apple",
    "4": "traxsource",
    "10": "soundcloud",
    "13": "video",
    "36": "spotify",
}

class trackList:
    '''
    Initialization automatically calls get_meta_data and get_track_data
    '''
    def __init__(self, url):
        self.url = url
        
        page = requests.get(url, headers = Headers().generate())
        self.soup = BeautifulSoup(page.text, 'html.parser')
        
        self.meta_data = self.get_meta_data()
        self.track_data = self.get_track_data()
    
    '''
    Gets meta data of tracklist on left sidebar of 1001tracklists pages
    '''
    def get_meta_data(self):
        meta_data = {}
        
        url_comp = self.url.split("/")
        meta_data["tracklist_id"] = url_comp[url_comp.index("tracklist") + 1]
        
        meta_data["tracklist_name"] = self.soup.find("h1", id = "pageTitle").text.strip()
        
        meta = self.soup.find("div", id = "leftDiv")
        
        try:
            meta_data["tracklist_date"] = meta.find("span", title = "tracklist recording date").parent.parent.select("td")[1].text
        except (AttributeError, IndexError):
            print(f"Couldn't find tracklist recording date")
        
        try:
            tracklist_interaction = meta.find_all("meta", itemprop = "interactionCount")
        except AttributeError:
            print(f"Couldn't find tracklist interactions")
        
        for interaction in tracklist_interaction:
            interaction_info = interaction["content"].strip().split(":")
            
            try:
                interaction_name = "tracklist_" + interaction_info[0].lower()
                interaction_count = interaction_info[1]
                meta_data[interaction_name] = interaction_count
            except IndexError:
                print(f"Couldn't find tracklist interaction value")
        
        try:
            IDed = re.search("\S+ \/ \S+", meta.text).group(0)
            IDed = IDed.split(" / ")
            meta_data["tracklist_tracks_IDed"] = IDed[0]
            meta_data["tracklist_tracks_total"] = IDed[1]
        except AttributeError:
            print(f"Couldn't find tracklist IDed")
        
        try:
            # Splits each genre into its own key with index
            tracklist_genres = meta.find("td", id = "tl_music_styles").text.split(", ")
            for i, genre in enumerate(tracklist_genres):
                meta_data["genre" + str(i)] = genre        
        except:
            print(f"Couldn't find tracklist genres")
        
        try:
            tracklist_DJs_location = meta.find_all("table", class_ = "sideTop")
            tracklist_DJs_location = [person_place.find("a") for person_place in tracklist_DJs_location]
            
            tracklist_DJs = []
            tracklist_source = {}
            
            for person_place in tracklist_DJs_location:
              if bool(re.search("\/dj\/", person_place.get("href"))):
                tracklist_DJs.append(person_place.text)
              
              if bool(re.search("\/source\/", person_place.get("href"))):
                tracklist_source[person_place.parent.parent.parent.find("td").contents[0]] = person_place.text
              
            # Splits each DJ into their own key with index
            for i, DJ in enumerate(tracklist_DJs):
                meta_data["DJ" + str(i)] = DJ
            
            # Tracklist sources include event name, location, radio show, etc.
            # Splits each by type of source
            for source in tracklist_source:
                source_number = 0
                source_w_number = source.strip() + str(source_number)
            
                while source_w_number in meta_data:
                    source_number += 1
                    source_w_number = source + str(source_number)
            
                meta_data[source_w_number] = tracklist_source[source]
            
        except AttributeError:
            print(f"Couldn't find tracklist sources (e.g. DJs, festival, radio show, etc.")
        
        return(meta_data)

    '''
    Gets all data in track table
    
    Includes track name, artist, url, 1001tracklists id, time played, track number, whether its a mashup and to what mashup it matches
    '''
    def get_track_data(self):
        tl_table = self.soup.find_all("tr", {"id": re.compile('tlp_[0-9]+')})
        
        tracks_info = []
        
        for cell in tl_table:
            track_info = {}
          
            for info in ["name", "byArtist", "url"]:
                try:
                    track_info[info] = cell.find("meta", itemprop = info).get("content")
                except AttributeError:
                    pass
        
              # 1001 Track ID
            try:
                tr_id = cell.find("span", {"id": re.compile('tr_([0-9]+)')}).get("id")
                track_info["id"] = re.search("tr_([0-9]+)", tr_id).group(1)
            except AttributeError:
                pass
          
            # Time in set played
            try:
                track_info["time"] = cell.find("div", {"class": "cueValueField action"}).text
            except AttributeError:
                pass
          
            # 1001 Track number or w/
            try:
                track_info["track_number"] = cell.find("span", {"id": re.compile("tracknumber_value")}).text
            except AttributeError:
                pass
        
            # Mashup and Mashup ID
            try:
                cell.find("td", class_ = "bootleg").text
                track_info["mashup"] = True
            except AttributeError:
                try:
                    cell.find("span", class_ = "mashupTrack").text
                    track_info["mashup"] = True
                    if tracks_info[-1]["name"]:
                        track_info["mashup_name"] = tracks_info[-1]["name"]
                    else:
                        track_info["mashup_name"] = "Name Missing"
                except AttributeError:
                    track_info["mashup"] = False
        
            tracks_info.append(track_info)
        
        return(tracks_info)
    
    '''
    Outputs both track data and meta data as a Pandas Data Frame
    '''
    def output_table(self):
        track_df = pd.DataFrame.from_dict(self.track_data)
        
        meta_df = pd.DataFrame([self.meta_data])
        meta_df_long = pd.concat([meta_df]*track_df.shape[0], ignore_index = True)
        
        return(pd.concat([meta_df_long, track_df], axis = 1))

'''
Gets the external media of a 1001Tracklists track by track id
'''
def get_external_media(tracklists_song_id):
    if not bool(re.match("\\d+", str(tracklists_song_id))):
        return(None)
    
    external_url = EXTERNAL_MEDIA_LINK.format(track_id = tracklists_song_id)
    response = requests.get(external_url).json()
    
    track_external_data = {}
    
    if response["success"]:
        data = response["data"]

        for media in data:
            try:
                source = SOURCES[media["source"]]
            except:
                source = "unknown_source"

            source_number = 0
            source_w_number = source + str(source_number)
        
            while source_w_number in track_external_data:
                source_number += 1
                source_w_number = source + str(source_number)
    
            try:
                track_external_data[source_w_number] = media["playerId"]
            except:
                pass
        
        return(track_external_data)
    
    else:
        return(None)








