import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_synthesizer import get_data

import pandas as pd
import numpy as np

from wordcloud import WordCloud

from io import BytesIO
import base64
import os
import string
import re

from urllib.parse import urlparse

def time_to_sec(time):
    
    if pd.isnull(time):
        return(np.nan)
    
    time_vals = time.split(":")[::-1]
    seconds = 0
    
    for i, time in enumerate(time_vals):
        seconds += int(time) * (60 ** i)
    
    return(seconds)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    style = {
        "background-image" : 'url("/assets/smiley-pattern1.jpg")',
        "background-repeate" : "repeat",
        "background-size" : "200px 200px"
        },
    
    children = [
        
        html.Section([
            html.Div([
                html.Div([
                    html.H1(children = "Tracklist Analyzer",
                            className = "title is-1"),
                    html.H2(children = "Discover how a set or playlist progresses",
                            className = "subtitle is-2")
                ], className='container'),
                
 			], className='hero-body')
		], className='hero is-small is-black'),
        
        html.Div([
            html.Div([
                html.Div([
                    html.H4(children = "Enter a tracklist URL from ",
                            className = "title is-4",
                            style = {"display" : "inline"}),
                    
                    html.A(children = "1001Tracklists.com",
                            href = "https://www.1001tracklists.com/",
                            target = "_blank",
                            className = "title is-4",
                            style = {"display" : "inline",
                                     "color" : "#3FAEF1"}),
                    
                    html.H4(children = " or select an example",
                            className = "title is-4",
                            style = {"display" : "inline"}),
                ], style = {'margin' : "0px 0px 12px 0px"}),
                
                html.Button(children = "Zeds Dead @ circuitGROUNDS",
                            id = "zeds_button",
                            n_clicks = 0,
                            className = "button is-black is-rounded",
                            style = {'margin': '0px 5px 10px 0px',
                                     "background-color" : '#248837'}),
                
                html.Button(children = "Hardwell @ Mainstage",
                            id = 'hardwell_button',
                            n_clicks = 0,
                            className = "button is-black is-rounded",
                            style = {'margin': '0px 5px 10px 0px',
                                     'background-color' : "#5F4889"}),
                
                html.Button(children = "Cosmic Gate @ ASOT Stage",
                            id = 'cosmic_button',
                            n_clicks = 0,
                            className = "button is-black is-rounded",
                            style = {'margin': '0px 5px 10px 0px',
                                     'background-color' : "#8C292B"}),
                
                html.Button(children = "Justice @ Google I/O",
                            id = 'justice_button',
                            n_clicks = 0,
                            className = "button is-black is-rounded",
                            style = {'margin': '0px 5px 10px 0px',
                                     'background-color' : '#B3905F'}),
                
                html.Button(children = "Seven Lions & Habstrakt - Night Owl Radio",
                            id = 'nightowl_button',
                            n_clicks = 0,
                            className = "button is-black is-rounded",
                            style = {'margin': '0px 5px 10px 0px',
                                     'background-color' : '#1D8F83'}),
                
                html.A(href = "https://github.com/AntonCitko/1001Tracklists-Visualizer/blob/master/README.md",
                       children = "Want info or need help?",
                       target="_blank",
                       className = "button is-black is-rounded",
                       style = {"margin" : "0px 0px 10px 0px",
                                "background-color" : "#F30000",
                                "float" : "right"}),
                
                html.Div(id = "input_control", 
                         children = [
                            dcc.Input(
                                id="user_input",
                                value =  "https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html",
                                type = "text",
                                placeholder = "Enter a tracklist URL from 1001Tracklists.com",
                                debounce = True,
                                className = "input",
                                style = {"border-color" : "yellow"}
                                ),
                ], className = "control",
                    style = {"margin" : "0px 0px 10px 0px"}),
                
                html.Div(id = "url_error_message",
                         children = [
                           html.H5(children = "URL does not match expected format. Expecting https://1001tracklsts.com/tracklists/`tracklist id`/`tracklist title`.html",
                            className = "subtitle is-5",
                            style = {'color' : 'red'}),
                           html.P(children = "")],
                        style = {"display" : "none"}),
                
                dcc.Loading(id = "loading_tracklist_data",
                            children = [html.H5(id = "tracklist_name_formatted",
                                                className = "subtitle is-5",
                                                style = {"white-space" : "pre"}),
                                        html.H6(id = "song_data_found_ratio",
                                                className = "subtitle is-5")],
                            type = "dot",
                            color = "black")
            ]),
        ], className= "box",
            style = {"margin" : "20px 20px 20px 20px",
                     "border-radius" : "0px"}),
        
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id = "tempo_graph"
                        ),
                ], className = "box",
                    style = {"margin" : "0px 0px 10px 0px",
                             "border-radius" : "0px"}),
                
                html.Div([
                    dcc.Graph(
                        id = "key_graph"
                        )
                ], className = "box",
                    style = {"margin" : "10px 0px 0px 0px",
                             "border-radius" : "0px",
                             "padding" : "0px"})
            ], className = "column",
                style = {"padding" : "0px",
                         "min-width" : "450px",
                         "margin" : "0px 10px 10px 10px"}),
            
            html.Div([
                html.Div([
                    html.Iframe(id = "spotify_play",
                                style = {"height" : "100%",
                                        "width" : "100%",
                                        "frameborder" : "0",
                                        "allowtransparency" : "True"})
                ], className = "is-hidden-touch",
                    style = {"height" : "490px",
                             "margin" : "0px 0px 10px 0px",
                             "background-color" : "black"}),
                html.Div([
                    html.Div([
                        html.P("Energy", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_energy")],
                            className="box",
                            style = {"width" : "30%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "0px 5px 5px 0px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Danceability", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_danceability")],
                            className="box",
                            style = {"width" : "35.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "0px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Valence", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_valence")],
                            className="box",
                            style = {"width" : "30%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "0px 0px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Instrumentalness", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_instrumentalness")],
                            className="box",
                            style = {"width" : "39.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 0px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Acousticness", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_acousticness")],
                            className="box",
                            style = {"width" : "28%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Speechiness", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_speechiness")],
                            className="box",
                            style = {"width" : "28%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 0px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Key", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_key")],
                            className="box",
                            style = {"width" : "22.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 0px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Mode", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_mode")],
                            className="box",
                            style = {"width" : "22.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Tempo", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_tempo")],
                            className="box",
                            style = {"width" : "22.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Duration", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_duration")],
                            className="box",
                            style = {"width" : "25.8%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 0px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Artist Genres", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_genres",
                                style = {"white-space" : "pre"})],
                            className="box",
                            style = {"width" : "100%",
                                     "height" : "150px",
                                     "display" : "inline-block",
                                     "margin" : "5px 0px 0px 0px",
                                     "border-radius" : "0px"}
                            )
                ], className = "is-hidden-touch"),

            ], className = "column is-hidden-touch",
               style = {"height" : "100%",
                        "min-width" : "450px",
                        "max-width" : "450px",
                        "margin" : "0px 10px 10px 10px",
                        "padding" : "0px"})
            
        ], className = "columns is-desktop",
            style = {"margin" : "0px 10px 0px 10px"}),
        
                        
                
            html.Div([
                html.Div([
                    html.Iframe(id = "spotify_play_mobile",
                                style = {"height" : "100%",
                                        "width" : "100%",
                                        "frameborder" : "0",
                                        "allowtransparency" : "True"})
                ], className = "column",
                    style = {"height" : "450px",
                             "margin" : "0px 10px 10px 10px",
                             "background-color" : "black"}),
                html.Div([
                    html.Div([
                        html.P("Energy", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_energy_mobile")],
                            className="box",
                            style = {"width" : "30%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "0px 5px 5px 0px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Danceability", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_danceability_mobile")],
                            className="box",
                            style = {"width" : "35.4%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "0px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Valence", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_valence_mobile")],
                            className="box",
                            style = {"width" : "30%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "0px 0px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Instrumentalness", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_instrumentalness_mobile")],
                            className="box",
                            style = {"width" : "39.4%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 0px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Acousticness", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_acousticness_mobile")],
                            className="box",
                            style = {"width" : "28%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Speechiness", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_speechiness_mobile")],
                            className="box",
                            style = {"width" : "28%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 0px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Key", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_key_mobile")],
                            className="box",
                            style = {"width" : "22.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 0px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Mode", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_mode_mobile")],
                            className="box",
                            style = {"width" : "22.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Tempo", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_tempo_mobile")],
                            className="box",
                            style = {"width" : "22.5%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 5px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Duration", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_duration_mobile")],
                            className="box",
                            style = {"width" : "25.7%",
                                     "height" : "90px",
                                     "display" : "inline-block",
                                     "margin" : "5px 0px 5px 5px",
                                     "border-radius" : "0px"}
                            ),
                    html.Div([
                        html.P("Artist Genres", 
                               style = {"font-weight" : "bold"}), 
                        html.H4(id = "sp_genres_mobile",
                                style = {"white-space" : "pre"})],
                            className="box",
                            style = {"width" : "100%",
                                     "height" : "150px",
                                     "display" : "inline-block",
                                     "margin" : "5px 0px 0px 0px",
                                     "border-radius" : "0px"}
                            )
                ], className = "column",
                    style = {"min-width" : "500px",
                             "margin" : "0px 10px 0px 0px",
                             "height" : "450px"})
            ], className = "columns is-hidden-desktop is-mobile",
                style = {"margin" : "10px 10px 0px 10px",
                         "padding" : "0px"}),
        
        html.Div([
            html.Div(id = "wordcloud_box",
                     children = [
                        html.Figure(className = "image", 
                                    children = [html.Img(id = "image_wc",
                                                         style = {"margins" : "auto",
                                                                  "max-height" : "500px"})],
                                    style = {"margin" : "auto",
                                             "max-height" : "500px"}),
            ], className = "box column",
                style = {"margin" : "0px 10px 10px 10px",
                         "border-radius" : "0px",
                         "padding" : "0px",
                         "height" : "500px",
                         "max-width" : "100%"}),

            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6("Average Song Tempo",
                                    className = "title is-6"),
                        ], className = "column"),
                                    
                        html.Div([
                            html.H6("Most Common Camelot Key",
                                    className = "title is-6"),
                        ], className = "column"),
        
                        html.Div([
                            html.H6("Average Song Loudness",
                                    className = "title is-6"),
                        ], className = "column"),
                    ], className = "columns has-text-centered",
                       style = {"width" : "100%",
                                "height" : "25%"}),
                    html.Div([
                        html.Div([
                            html.P(id = "avg_tempo")
                        ], className = "column"),
                                    
                        html.Div([
                            html.P(id = "avg_camelot")
                        ], className = "column"),
        
                        html.Div([
                            html.P(id = "avg_loud")
                        ], className = "column"),
                    ], className = "columns has-text-centered",
                       style = {"width" : "100%",
                                "height" : "50px",
                                "margin" : "12px 0px 0px 0px"})
                
                ], className = "box",
                   style = {"border-radius" : "0px",
                            "width" : "100%",
                            "height" : "110px",
                            "padding" : "30px 20px 20px 20px",
                            "margin" : "0px 0px 10px 0px"}),
                            
                html.Div([
                    dcc.Graph(id = "avg_metrics")
                ],  className = "box",
                    style = {"width" : "100%",
                            "height" : "380px",
                            "border-radius" : "0px",
                            "padding" : "12px"})
                
            ], className="column",
                style = {"margin" : "0px 10px 10px 10px",
                         "height" : "500px",
                         "min-width" : "725px",
                         "max-width" : "100%",
                         "padding" : "0px"})
        ], className="columns is-desktop",
            style = {"margin" : "10px 10px 0px 10px",
                     "padding" : "0px 0px 20px 0px"}),
    
        
        html.Div(id='tracklist_name', style = {'display' : 'none'}),
        html.Div(id='tracklist_data', style={'display': 'none'}),
        html.Div(id='tracklist_data_clean', style={'display': 'none'}),
        html.Div(id='tracklist_data_missing', style={'display': 'none'}),
        html.Div(id='song_genres', style={'display': 'none'}),
        html.Div(id='tracklist_metrics_mean', style={'display': 'none'}),
        html.Div(id="song_clicked", style={"display":"none"}),
        html.Div(id="size", style={"display":"none"}),
        html.Div(id="checked_url", style={"display" : "none"}),
        html.Div(id="input_url", style={"display": "none"}),
        dcc.Location(id="url")
    ]) 

@app.callback(
    Output("user_input", "value"),
    [Input("zeds_button", "n_clicks"),
     Input("hardwell_button", "n_clicks"),
     Input("cosmic_button", "n_clicks"),
     Input("justice_button", "n_clicks"),
     Input("nightowl_button", "n_clicks")]
)
def update_example(zeds, hardwell, cosmic, justice, nightowl):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    example_buttons = {"." : "https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html",
                        "zeds_button.n_clicks" : "https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html",
                        "hardwell_button.n_clicks" : "https://www.1001tracklists.com/tracklist/1ldcw1rk/hardwell-mainstage-ultra-music-festival-miami-united-states-2016-03-19.html",
                        "cosmic_button.n_clicks" : "https://www.1001tracklists.com/tracklist/1r4qp141/cosmic-gate-asot-stage-tomorrowland-weekend-2-belgium-2019-07-28.html",
                        "justice_button.n_clicks" : "https://www.1001tracklists.com/tracklist/zu8mtf9/justice-google-islasho-united-states-2018-05-10.html",
                        "nightowl_button.n_clicks" : "https://www.1001tracklists.com/tracklist/2l5u0mu9/seven-lions-habstrakt-night-owl-radio-245-2020-04-24.html"}
    
    url = example_buttons[changed_id]
    
    return(url)

@app.callback(
    [Output("checked_url", "children"),
     Output("url_error_message", "style")],
    [Input("user_input", "value")]
)
def check_url(url):
    url_scheme = urlparse(url)
    
    if url_scheme.netloc == "www.1001tracklists.com" and url_scheme.path.split("/")[1] == "tracklist":
        return(url, {"display" : "none"})
    
    else:
        return(url, {"display" : "inline"})
    
@app.callback(
    Output("input_url", "children"),
    [Input("checked_url", "children"),
     Input("url_error_message", "style")]
)
def continue_good_url(url, error_style):
    if error_style["display"] == "inline":
        raise PreventUpdate("Bad URL")
    
    return(url)

@app.callback(
    [Output("tracklist_name", "children"),
    Output("tracklist_name_formatted", "children"),
    Output("tracklist_data", "children"),
    Output("tracklist_data_clean", "children"),
    Output("tracklist_data_missing", "children"),
    Output("song_genres", "children"),
    Output("tracklist_metrics_mean", "children"),
    Output("avg_tempo", "children"),
    Output("avg_loud", "children"),
    Output("song_data_found_ratio", "children")],
    [Input("input_url", "children")]
)
def update_url(url):
    
    example_urls = {"https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html" : "zeds_dead_example.csv",
                    "https://www.1001tracklists.com/tracklist/1r4qp141/cosmic-gate-asot-stage-tomorrowland-weekend-2-belgium-2019-07-28.html" : "cosmic_gate_example.csv",
                    "https://www.1001tracklists.com/tracklist/zu8mtf9/justice-google-islasho-united-states-2018-05-10.html" : "justice_example.csv",
                    "https://www.1001tracklists.com/tracklist/2l5u0mu9/seven-lions-habstrakt-night-owl-radio-245-2020-04-24.html" : "night_owl_radio_example.csv",
                    "https://www.1001tracklists.com/tracklist/1ldcw1rk/hardwell-mainstage-ultra-music-festival-miami-united-states-2016-03-19.html" : "hardwell_example.csv"}
    
    if url in example_urls:
        
        print("reading example")
        
        data = pd.read_csv(os.path.join(os.getcwd(), "assets", example_urls[url]))
    
    else:
        print("getting data")
        
        data = get_data(url)
    
        print("gotten data")
    
    tracklist_name = data.iloc[0]["tracklist_name"]
    
    tracklist_name_formatted = "\n".join(re.split(" - |, ", tracklist_name))
    
    if "time" not in data or data["time"].str.isspace().all():
        data["time"] = [str(i) + ":00" for i in range(data.shape[0])]
    
    data["time"] = data["time"].replace(r'^\s*$', np.nan, regex=True)
    data["time"] = data["time"].ffill()
    
    data["time"] = data["time"].str.strip()
    data["seconds"] = data["time"].apply(time_to_sec)
    
    data_missing = data[data["tempo"].isnull()]
    
    data_clean = data.dropna(subset = ["tempo"])
    
    song_genres = data["genres"].dropna().to_list()
    song_genres = [genre for genre_list in song_genres for genre in genre_list.split(",") if genre]
    
    data_metric_mean = data_clean[["acousticness", "instrumentalness", "speechiness", "danceability", "energy", "valence"]].mean()
    
    avg_tempo = str(round(data_clean["tempo"].mean(), 0)) + " BPM"
    
    avg_loud = str(round(data_clean["loudness"].mean(), 2)) + " dB"
    
    songs_total = data.shape[0]
    songs_found = data_clean.shape[0]
    
    song_data_found_ratio = "Found " + str(songs_found) + " of " + str(songs_total) + " songs"
    
    return(tracklist_name, tracklist_name_formatted, data.to_json(), data_clean.to_json(), data_missing.to_json(), song_genres, data_metric_mean.to_json(), avg_tempo, avg_loud, song_data_found_ratio)

    
@app.callback(
    Output("tempo_graph", "figure"),
    [Input("tracklist_data_clean", "children")]
)
def update_tempo_graph(data):    
    data = pd.read_json(data)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x = data.seconds,
                    y = data.energy.rolling(3, min_periods = 1, center = True).mean(),
                    name = "Energy",
                    line_shape = "spline",
                    line = dict(smoothing = 1.3,
                                color = "#542bc4"),
                    hoverinfo = "skip"),
        secondary_y = False,
    )
    
    fig.add_trace(
        go.Scatter(x = data.seconds,
                    y = data.danceability.rolling(3, min_periods = 1, center = True).mean(),
                    name = "Danceability",
                    line_shape = "spline",
                    line = dict(smoothing = 1.3,
                                color = "#2b72c4"),
                    hoverinfo = "skip"),
        secondary_y = False,
    )
    
    fig.add_trace(
        go.Scatter(x = data.seconds,
                    y = data.valence.rolling(3, min_periods = 1, center = True).mean(),
                    name = "Valence",
                    line_shape = "spline",
                    line = dict(smoothing = 1.3,
                                color = "#C42BBF"),
                    hoverinfo = "skip"),
        secondary_y = False,
    )
    
    data_tempo_mean = data.groupby("seconds")["tempo"].mean()
    
    fig.add_trace(
        go.Scatter(x = data_tempo_mean.index,
                    y = data_tempo_mean,
                    name = "Tempo",
                    line_shape = "spline",
                    line = dict(width = 5,
                                color = "#2bc47d"),
                    hoverinfo = "skip"),
        secondary_y = True
    )
    
    hovertemplate_tempo = """<b>%{customdata[0]}</b><br>Tempo: %{customdata[1]}<br>Energy: %{customdata[2]}<br>Danceability: %{customdata[3]}<br>Valence: %{customdata[4]}"""
    
    fig.add_trace(
        go.Scatter(x = data.seconds,
                    y = data.tempo,
                    customdata = data[["name", "tempo", "energy", "danceability", "valence", "spotify0"]].round(2),
                    name = "Song",
                    mode = "markers",
                    marker = dict(size = 10,
                                  color = "#212120"),
                    hovertemplate = hovertemplate_tempo,
                    hoverlabel = dict(bgcolor = "white",
                                      bordercolor = "white",
                                      font_color = "black",
                                      namelength = 0)),
        secondary_y = True
    )
    
    
    
    # Add figure title
    fig.update_layout(
        title_text="Song Tempo and Spotify Metrics",
        xaxis = dict(
            showline = True,
            showgrid = False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=11,
                color='rgb(82, 82, 82)'),
            tickmode = "array",
            tickvals = data.seconds,
            ticktext = data.time,
            tickangle = 65,
            showspikes = True,
            spikemode = "across",
            spikethickness = 2
            ),
        yaxis = dict(
            showgrid = False,
            side = "right"),
        yaxis2 = dict(
            showgrid = False,
            side = "left"),
        plot_bgcolor = "white",
        hovermode = "closest"
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text="Time")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Spotify Value", secondary_y=False)
    fig.update_yaxes(title_text="Beats per Minute", secondary_y=True)
    
    return(fig)

@app.callback(
    [Output("key_graph", "figure"),
     Output("avg_camelot", "children")],
    [Input("tracklist_data_clean", "children")]
)
def update_key_graph(data):
    data = pd.read_json(data)
    
    data = data[data["key"] != -1]
    
    pitch_to_cam = {(0,1):'8B',
            		(1,1):'3B',
            		(2,1):'10B',
            		(3,1):'5B',
            		(4,1):'12B',
            		(5,1):'7B',
            		(6,1):'2B',
            		(7,1):'9B',
            		(8,1):'4B',
            		(9,1):'11B',
            		(10,1):'6B',
            		(11,1):'1B',
            		(0,0):'5A',
            		(1,0):'12A',
            		(2,0):'7A',
            		(3,0):'2A',
            		(4,0):'9A',
            		(5,0):'4A',
            		(6,0):'11A',
            		(7,0):'6A',
            		(8,0):'1A',
            		(9,0):'8A',
            		(10,0):'3A',
            		(11,0):'10A'}
    
    pitch_to_cam = {" ".join([str(key[0]), str(key[1])]) : pitch_to_cam[key] for key in pitch_to_cam}
    
    data["camelot"] = data["key"].astype(int).astype(str) + " " + data["mode"].astype(int).astype(str)
    
    data = data.replace({"camelot": pitch_to_cam})
    avg_camelot = " ".join(data["camelot"].mode())
    
    data["camelot_num"] = data["camelot"].str.strip(string.ascii_letters)
    data["camelot_let"] = data["camelot"].str.strip(string.digits)
    
    cam_col_A = "#E95555"
    cam_col_B = "#55E9E9"
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    data_key_mean = data.groupby("seconds")["key"].mean()
    data_loudness_mean = data.groupby("seconds")["loudness"].mean()
    
    show_in_legend_A = True
    show_in_legend_B = True
    for sec0, key0, sec1, key1, letter in zip(data["seconds"].to_list(), data["camelot_num"].to_list(), data.iloc[1:]["seconds"].to_list() + [None], data.iloc[1:]["camelot_num"].to_list() + [None], data["camelot_let"].to_list()):
        
        if not sec1:
            sec1 = sec0 + 60
            key1 = key0
        
        key0 = int(key0)
        key1 = int(key1)
        
        col = letter.replace("A", cam_col_A).replace("B", cam_col_B)
        
        if letter == "A":
            leg_name = "Camelot Letter A"
            show_leg = show_in_legend_A
        if letter == "B":
            leg_name = "Camelot Letter B"
            show_leg = show_in_legend_B
        
        fig.add_trace(
                go.Scatter(x = [sec0, sec1],
                           y = [key0, key0],
                           mode = "lines",
                           line = dict(width = 5,
                                       color = col),
                           hoverinfo = "skip",
                           name = leg_name,
                           showlegend = show_leg),
                secondary_y = True)
        
        if key0 < key1:
            key0 -= 0.12
            key1 += 0.12
        else:
            key0 += 0.12
            key1 -= 0.12
        
        fig.add_trace(
                go.Scatter(x = [sec1, sec1],
                           y = [key0, key1],
                           mode = "lines",
                           line = dict(width = 5,
                                       color = col),
                           hoverinfo = "skip",
                           showlegend = False),
                secondary_y = True)
        
        if letter == "A":
            show_in_legend_A = False
        if letter == "B":
            show_in_legend_B = False
    
    
    hovertemplate_tempo = """<b>%{customdata[0]}</b><br>Camelot Value: %{customdata[1]}<br>Loudness: %{customdata[2]}"""
    
    fig.add_trace(
        go.Scatter(x = data.seconds,
                    y = data.camelot_num,
                    customdata = data[["name", "camelot", "loudness", "spotify0"]].round(2),
                    name = "Song",
                    mode = "markers",
                    showlegend = False,
                    marker = dict(size = 10,
                                  color = "#212120"),
                    hovertemplate = hovertemplate_tempo,
                    hoverlabel = dict(bgcolor = "white",
                                      bordercolor = "white",
                                      font_color = "black",
                                      namelength = 0)),
            secondary_y = True)
    
    
    fig.add_trace(
        go.Scatter(x = data_loudness_mean.index,
                    y = data_loudness_mean,
                    name = "Loudness",
                    line_shape = "spline",
                    line = dict(color = "#212120"),
                    hoverinfo = "skip"),
    )
        
    fig.add_trace(
        go.Scatter(x = data_loudness_mean.index,
                    y = [data_loudness_mean.min()] * len(data_loudness_mean),
                    line_shape = "spline",
                    line = dict(color = "#FFFFFF"),
                    fill = "tonexty",
                    fillcolor = "#888888",
                    showlegend = False,
                    hoverinfo = "skip"),
    )
    
    # Add figure title
    fig.update_layout(
        title_text="Harmonic Mixing and Loudness",
        xaxis = dict(
            showline = True,
            showgrid = False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=11,
                color='rgb(82, 82, 82)'),
            tickmode = "array",
            tickvals = data.seconds,
            ticktext = data.time,
            tickangle = 65,
            showspikes = True,
            spikemode = "across",
            spikethickness = 2
            ),
        yaxis = dict(
            showgrid = False,
            side = "right"),
        yaxis2 = dict(
            showgrid = False,
            side = "left"),
        plot_bgcolor = "white"
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text="Time")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Camelot Number", secondary_y=True)
    fig.update_yaxes(title_text="Decibels", secondary_y=False)
    
    return(fig, avg_camelot)

@app.callback(
    Output("avg_metrics", "figure"),
    [Input("tracklist_metrics_mean", "children")]
)
def update_tracklist_metrics_mean(metrics_mean):
    METRICS_NAME = ["Energy", "Danceability", "Valence",
                    "Acousticness", "Instrumentalness", "Speechiness"]
    
    METRICS_COLORS = ["#542bc4", "#2b72c4", "#C42BBF",
                      "#212120", "#A02BC4"," #C42B4E"]
    
    metrics_mean = pd.read_json(metrics_mean, lines = True)
    
    metrics_mean = metrics_mean.iloc[0].to_dict()
    
    fig = make_subplots(2, 3, 
                        specs = [[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
                                 [{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
                        subplot_titles = METRICS_NAME)
    
    metric_vals = []
    
    for i, metric in enumerate(METRICS_NAME):
        val = metrics_mean[metric.lower()]
        
        fig.add_trace(
            go.Pie(values = [1 - val, val], 
                   name = metric,
                   textinfo = "none",
                   # marker_colors = ["white", "red"],
                   direction = "clockwise",
                   sort = False,
                   marker = dict(colors = ["white", METRICS_COLORS[i]],
                                 line = dict(color = METRICS_COLORS[i],
                                 width = 0.75))),
            row = i//3 + 1, col = (i % 3) + 1)
        
        metric_vals.append(round(val, 2))
    
    fig.update_traces(hole = 0.65, 
                      hoverinfo = "skip")
    
    fig.update_layout(showlegend = False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      margin = dict(l = 20, r = 20, b = 100, t = 25, pad = 0),
                      annotations = fig["layout"]["annotations"] + (dict(text = "{:.2f}".format(metric_vals[0]), x = 0.118, y = 0.857, font_size = 16, showarrow = False),
                                                                    dict(text = "{:.2f}".format(metric_vals[1]), x = 0.5, y = 0.857, font_size = 16, showarrow = False),
                                                                    dict(text = "{:.2f}".format(metric_vals[2]), x = 0.885, y = 0.857, font_size = 16, showarrow = False),
                                                                    dict(text = "{:.2f}".format(metric_vals[3]), x = 0.118, y = 0.153, font_size = 16, showarrow = False),
                                                                    dict(text = "{:.2f}".format(metric_vals[4]), x = 0.5, y = 0.153, font_size = 16, showarrow = False),
                                                                    dict(text = "{:.2f}".format(metric_vals[5]), x = 0.885, y = 0.153, font_size = 16, showarrow = False)))
    
    return(fig)
    

app.clientside_callback(
    """
    function(input_url, url) {
        var elmnt = document.getElementById("wordcloud_box");
        var width = elmnt.offsetWidth;
        //width = window.innerWidth;
        
        return(width);
    }
    """,
    Output('size', 'children'),
    [Input('input_url', 'children'),
     Input("url", "href")]
)

@app.callback(
    Output('image_wc', 'src'), 
    [Input('song_genres', 'children'),
     Input("size", "children")]
)
def make_word_cloud(song_genres, width):
    song_genres_dict = pd.Series(song_genres).value_counts().to_dict()

    wordcloud = WordCloud(background_color = "white", 
                          relative_scaling = 0.175,
                          height = 500,
                          width = width,
                          scale = 1,
                          repeat = True, 
                          max_words = 300,
                          min_font_size = 3).generate_from_frequencies(song_genres_dict)
    
    image = wordcloud.to_image()
        
    img = BytesIO()
    image.save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(
    [Output("song_clicked", "children"),
     Output("spotify_play", "src"),
     Output("sp_energy", "children"),
     Output("sp_danceability", "children"),
     Output("sp_valence", "children"),
     Output("sp_acousticness", "children"),
     Output("sp_instrumentalness", "children"),
     Output("sp_speechiness", "children"),
     Output("sp_key", "children"),
     Output("sp_mode", "children"),
     Output("sp_tempo", "children"),
     Output("sp_genres", "children"),
     Output("sp_duration", "children"),
     
     Output("spotify_play_mobile", "src"),
     Output("sp_energy_mobile", "children"),
     Output("sp_danceability_mobile", "children"),
     Output("sp_valence_mobile", "children"),
     Output("sp_acousticness_mobile", "children"),
     Output("sp_instrumentalness_mobile", "children"),
     Output("sp_speechiness_mobile", "children"),
     Output("sp_key_mobile", "children"),
     Output("sp_mode_mobile", "children"),
     Output("sp_tempo_mobile", "children"),
     Output("sp_genres_mobile", "children"),
     Output("sp_duration_mobile", "children")],
    [Input("tracklist_data_clean", "children"),
     Input("tempo_graph", "clickData"),
     Input("key_graph", "clickData")]
)
def update_song(data, click_data_tempo, click_data_key):
    ctx = dash.callback_context
    
    data = pd.read_json(data)
    
    SPOTIFY_EMBED_URL_PREFIX = "https://open.spotify.com/embed/track/"
    SP_METRICS = ["energy", "danceability", "valence", "acousticness", "instrumentalness", "speechiness", "key", "mode", "tempo", "genres", "duration_ms"]
    
    if ctx.triggered[0]["prop_id"] == "tracklist_data_clean.children":
        spotify_default_song = data.iloc[0][["name", "spotify0"]].to_list()
        
        song_clicked_name = spotify_default_song[0]
        song_clicked_id = spotify_default_song[1]
        
    else:
        clicked_data = ctx.triggered[0]["value"]["points"][0]["customdata"]
        song_clicked_name = clicked_data[0]
        song_clicked_id = clicked_data[-1]
    
    song_spotify_embed = SPOTIFY_EMBED_URL_PREFIX + song_clicked_id
    
    song_spotify_metrics = data[data["name"] == song_clicked_name].iloc[[0]][SP_METRICS]
    
    # Convert milliseconds to time
    millis = int(song_spotify_metrics["duration_ms"])
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    hours = int(hours)
    
    if hours == 0:
        song_spotify_metrics["duration_ms"] = "{}:{:02d}".format(minutes, seconds)
    else:
        song_spotify_metrics["duration_ms"] = "{}:{}:{:02d}".format(hours, minutes, seconds)
        
    if song_spotify_metrics["genres"].values[0]:
        # Format genres
        sp_artist_genres = song_spotify_metrics["genres"].values[0].split(",")
        
        for i in range(len(sp_artist_genres) - 1):
            if (i + 1) % 3 == 0:
                sp_artist_genres[i] += "\n"
            else:
                sp_artist_genres[i] += " | "
        
        song_spotify_metrics["genres"] = "".join(sp_artist_genres)
    else:
        song_spotify_metrics["genres"] = "No Artist Genres Found on Spotify"
    
    song_spotify_metrics = tuple(song_spotify_metrics.round(2).values.tolist()[0])
    
    return(song_clicked_name, song_spotify_embed, *song_spotify_metrics, song_spotify_embed, *song_spotify_metrics)


if __name__ == "__main__":
    app.run_server(debug = True, use_reloader = False)