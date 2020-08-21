import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import pandas as pd

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
        
        meta = self.soup.find("div", id = "leftDiv")
        
        meta_data["tracklist_date"] = meta.find("span", title = "tracklist recording date").parent.parent.select("td")[1].text
        
        tracklist_interaction = meta.find_all("meta", itemprop = "interactionCount")
        meta_data["tracklist_views"] = tracklist_interaction[0]["content"].split(":")[1]
        meta_data["tracklist_likes"] = tracklist_interaction[1]["content"].split(":")[1]
        
        IDed = re.search("\S+ \/ \S+", meta.text).group(0)
        IDed = IDed.split(" / ")
        meta_data["tracklist_tracks_IDed"] = IDed[0]
        meta_data["tracklist_tracks_total"] = IDed[1]
        
        # Splits each genre into its own key with index
        tracklist_genres = meta.find("td", id = "tl_music_styles").text.split(", ")
        for i, genre in enumerate(tracklist_genres):
            meta_data["genre" + str(i)] = genre
        
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
          source_w_number = source + str(source_number)
        
          while source_w_number in meta_data:
            source_number += 1
            source_w_number = source + str(source_number)
        
        meta_data[source_w_number] = tracklist_source[source]
        
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

