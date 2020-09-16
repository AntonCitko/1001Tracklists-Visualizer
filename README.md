# 1001Tracklists Visualizer
The goal of this project is to create a dashboard that visualizes tracklists from 1001Tracklists.com

### A running version of the dashboard can be found on Heroku at:  
### https://tracklists-visualizer.herokuapp.com/

## How to use
* Enter a tracklist URL from 1001Tracklists.com into the search bar or select an example tracklist
* Click on data points to view a song's Spotify metrics as well as listen to a preview
* Graphs are fully interactable and can be filtered by clicking a line in their legend or zoomed using the graph's toolbar
* At the bottom of the dashboard is a Wordcloud of the songs' genres on Spotify in addition to the average metrics for the entire tracklist

## Notes
* The app works by pulling song features from Spotify's API so tracklists without Spotify links for their songs will be incomplete
  * This also means that the data only represents the original song's features and not how the DJ played it (e.g. a song is sped up or pitched down)
* Song timestamps are pulled from the tracklist, so if the tracklist lacks timestamps the graphs may be inaccurate
* More information on Spotify's song metrics can be found at: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
* More information on harmonic mixing and the Camelot Wheel can be found at: https://mixedinkey.com/harmonic-mixing-guide/

## To-Do
- [ ] Ability to handle Spotify playlists in addition to 1001Tracklists
  - [ ] Playlist creation from tracklist
