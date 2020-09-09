# 1001Tracklists Visualizer
The goal of this project is to create a dashboard that visualizes tracklists from 1001Tracklists.com

### A running version of the dashboard can be found on Heroku at:  
### https://tracklists-visualizer.herokuapp.com/

## How to use
* Enter a tracklist URL from 1001Tracklists.com into the search bar
* Click songs on the graphs to view its specific metrics

## Notes
* The app works by pulling song features from Spotify's API so tracklists' without Spotify links for their songs will be incomplete
* More information on Spotify's song metrics can be found at: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
* More information on the Camelot Wheel can be found at: https://mixedinkey.com/harmonic-mixing-guide/

## To-Do
- [ ] Ability to handle Spotify playlists in addition to 1001Tracklists
- [ ] Add in more example links
- [ ] Style dashboard to handle varying sized displays
