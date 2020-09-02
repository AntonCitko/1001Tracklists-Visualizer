import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_synthesizer import get_data

import pandas as pd
import numpy as np

from wordcloud import WordCloud

# import dash
# import dash.dependencies as dd
# import dash_core_components as dcc
# import dash_html_components as html

from io import BytesIO

import base64

import tabulate

import os

#%%

# url = "https://www.1001tracklists.com/tracklist/2rskz669/jstjr-kill-the-noise-night-owl-radio-243-2020-04-11.html"

#url = "https://www.1001tracklists.com/tracklist/2vhlqun9/louis-the-child-alison-wonderland-night-owl-radio-236-2020-02-22.html"

# url= "https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html"

# data = get_data(url)

#%%

def time_to_sec(time):
    time_vals = time.split(":")[::-1]
    seconds = 0
    
    for i, time in enumerate(time_vals):
        seconds += int(time) * (60 ** i)
    
    return(seconds)

#%%

app = dash.Dash(__name__)

app.layout = html.Div(
    style = {
        "background-image" : 'url("/assets/smiley.png")',
        "background-repeate" : "repeat-y",
        "background-size" : "100px 100px"
        },
    
    children = [
        
        html.Section([
            html.Div([
                html.Div([
                    html.H1(children = "1001Tracklists by the Numbers",
                            className = "title"),
                    html.H2(children = "1001Tracklists by the Numbers",
                            className = "subtitle")
                ], className='container'),
                
                html.Div([
                    dcc.Input(
                        id="input_url",
                        value =  "https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html",
                        type = "text",
                        placeholder = "Enter a tracklist URL from 1001Tracklists.com",
                        debounce = True
                        ),
                
                    html.Div(id = "tracklist_name"),
                
                    html.H2(children = "set"),
                ])
 			], className='hero-body')
		], className='hero is-dark'),
        
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id = "tempo_graph"
                        ),
                ], className = "box",
                    style = {"margin" : "10px 0px 20px 20px"}),
                
                html.Div([
                    dcc.Graph(
                        id = "key_graph"
                        )
                ], className = "box",
                    style = {"margin" : "0px 0px 10px 20px"})
            ], className = "column is-three-quarters"),
            
            html.Div([
                html.Div([
                    html.Iframe(id = "spotify_play",
                                style = {"height" : "80px",
                                        "width" : "100%",
                                        "frameborder" : "0",
                                        "allowtransparency" : "True"})
                ], style = {"width" : "95%",
                             "height" : "490px",
                             "margin" : "10px"}),
                html.Div([
                    html.Div([
                        html.P("Energy"), html.H4(id = "sp_energy")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Danceability"), html.H4(id = "sp_danceability")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Valence"), html.H4(id = "sp_valence")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Acousticness"), html.H4(id = "sp_acousticness")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Instrumentalness"), html.H4(id = "sp_instrumentalness")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Speechiness"), html.H4(id = "sp_speechiness")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Key"), html.H4(id = "sp_key")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Mode"), html.H4(id = "sp_mode")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Tempo"), html.H4(id = "sp_tempo")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Artist Genres"), html.H4(id = "sp_genres")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            ),
                    html.Div([
                        html.P("Duration"), html.H4(id = "sp_duration")],
                            className="box",
                            style = {"width" : "auto",
                                     "display" : "inline-block",
                                     "margin" : "5px"}
                            )
                ])
            ], className = "column",
               style = {"height" : "100%",
                        "width" : "100%"})
            
        ], className = "columns",
            style = {"height" : "1100px"}),
        
        html.Div([
            html.Div([
                html.H3('Song Genres Word Cloud'),
                html.Img(id = "image_wc"),
            ], className="two columns",
                style = dict(display = "inline-block", align = "left")),
    
            html.Div([
                html.Div([
                    html.P("Energy"), html.H4(id = "avg_energy")],
                        className="mini_container",
                        ),
                html.Div([
                    html.P("Danceability"), html.H4(id = "avg_danceability")],
                        className="mini_container",
                        ),
                html.Div([
                    html.P("Valence"), html.H4(id = "avg_valence")],
                        className="mini_container",
                        ),
                html.Div([
                    html.P("Acousticness"), html.H4(id = "avg_acousticness")],
                        className="mini_container",
                        ),
                html.Div([
                    html.P("Instrumentalness"), html.H4(id = "avg_instrumentalness")],
                        className="mini_container",
                        ),
                html.Div([
                    html.P("Speechiness"), html.H4(id = "avg_speechiness")],
                        className="mini_container",
                        )
            ], className="three columns",
                style = dict(width = "65%", display = "inline-block", align = "right"))
        ], className="row", 
            style = dict(display = "flex")),
        
        html.Div(id='tracklist_data', style={'display': 'none'}),
        html.Div(id='tracklist_data_clean', style={'display': 'none'}),
        html.Div(id='tracklist_data_missing', style={'display': 'none'}),
        html.Div(id='song_genres', style={'display': 'none'}),
        html.Div(id='tracklist_metrics_mean', style={'display': 'none'}),
        html.Div(id='spotify_default_song', style={'display': 'none'}),
        html.Div(id="song_clicked", style={"display":"none"})
    ])

@app.callback(
    [Output("tracklist_name", "children"),
    Output("tracklist_data", "children"),
    Output("tracklist_data_clean", "children"),
    Output("tracklist_data_missing", "children"),
    Output("song_genres", "children"),
    Output("tracklist_metrics_mean", "children"),
    Output("spotify_default_song", "children")],
    [Input("input_url", "value")]
)
def update_url(url):
    tracklist_name = url
    
    if url == "https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html":
        
        print("reading example")
        
        data = pd.read_csv(os.path.join(os.getcwd(), "assets", "zeds_example.csv"))
    
    else:
        print("getting_data")
        
        data = get_data(url)
    
        print("gotten_data")
    
    data["time"] = data["time"].replace(r'^\s*$', np.nan, regex=True)
    data["time"] = data["time"].ffill()
    data["time"] = data["time"].str.strip()
    data["seconds"] = data["time"].apply(time_to_sec)
    
    data_missing = data[data["tempo"].isnull()]
    
    data_clean = data.dropna(subset = ["tempo"])
    
    song_genres = data["genres"].dropna().to_list()
    song_genres = [genre for genre_list in song_genres for genre in genre_list.split(",") if genre]
    
    data_metric_mean = data_clean[["acousticness", "instrumentalness", "speechiness", "danceability", "energy", "valence"]].mean()
    
    spotify_default_song = data.iloc[0][["name", "spotify0"]].to_list()
    
    return(tracklist_name, data.to_json(), data_clean.to_json(), data_missing.to_json(), song_genres, data_metric_mean.to_json(), spotify_default_song)

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
        title_text="Time Metrics",
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
    Output("key_graph", "figure"),
    [Input("tracklist_data_clean", "children")]
)
def update_key_graph(data):
    data = pd.read_json(data)
    
    # mode_colors = ["#212120" if mode == 0 else "#2b72c4" for mode in data["mode"]]
    
    data = data.replace({"mode": 
                         {0 : "#212120",
                          1 : "#2b72c4"}})
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    data_key_mean = data.groupby("seconds")["key"].mean()
    data_loudness_mean = data.groupby("seconds")["loudness"].mean()
    
    # fig.add_trace(
    #     go.Scatter(x = data_key_mean.index,
    #                 y = data_key_mean,
    #                 name = "Key",
    #                 line_shape = "spline",
    #                 line = dict(width = 5,
    #                             color = "#2bc47d")),
    #     secondary_y = True
    # )
    
    fig.add_trace(
        go.Scatter(x = data.seconds,
                    y = data.key,
                    name = "Key",
                    line_shape = "hv",
                    line = dict(width = 5,
                                color = "#2bc47d"),
                    hoverinfo = "skip"),
        secondary_y = True
    )
    
    hovertemplate_tempo = """<b>%{customdata[0]}</b><br>Key: %{customdata[1]}<br>Loudness: %{customdata[2]}"""
    
    fig.add_trace(
        go.Scatter(x = data.seconds,
                    y = data.key,
                    customdata = data[["name", "key", "loudness", "spotify0"]].round(2),
                    name = "Mode",
                    mode = "markers",
                    marker = dict(size = 10,
                                  color = data["mode"]),
                    hovertemplate = hovertemplate_tempo,
                    hoverlabel = dict(bgcolor = "white",
                                      bordercolor = "white",
                                      font_color = "black",
                                      namelength = 0)),
        secondary_y = True
    )
    
    
    fig.add_trace(
        go.Scatter(x = data_loudness_mean.index,
                    y = data_loudness_mean,
                    name = "Loudness",
                    line_shape = "spline",
                    line = dict(color = "#212120"),
                    hoverinfo = "skip")
    )
        
    fig.add_trace(
        go.Scatter(x = data_loudness_mean.index,
                    y = [data_loudness_mean.min()] * len(data_loudness_mean),
                    line_shape = "spline",
                    line = dict(color = "#FFFFFF"),
                    fill = "tonexty",
                    fillcolor = "#888888",
                    showlegend = False,
                    hoverinfo = "skip")
    )
    # fig.add_trace(
    #     go.Scatter(x = [0, data.seconds.max()],
    #                 y =[-100, -100],
    #                 name = "Loudness",
    #                 line_shape = "spline",
    #                 line = dict(color = "#212120"),
    #                 fill = "toself")
    # )
    
    
    # Add figure title
    fig.update_layout(
        title_text="Key and Loudness",
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
    fig.update_yaxes(title_text="Decibels", secondary_y=False)
    fig.update_yaxes(title_text="Key in Pitch Class Notation", secondary_y=True)
    
    return(fig)

@app.callback(
    [Output("avg_energy", "children"),
     Output("avg_danceability", "children"),
     Output("avg_valence", "children"),
     Output("avg_acousticness", "children"),
     Output("avg_instrumentalness", "children"),
     Output("avg_speechiness", "children")],
    [Input("tracklist_metrics_mean", "children")]
)
def update_tracklist_metrics_mean(metrics_mean):
    metrics_mean = pd.read_json(metrics_mean, lines = True)
    
    return(float(metrics_mean["energy"].round(3)),
           float(metrics_mean["danceability"].round(3)), 
           float(metrics_mean["valence"].round(3)), 
           float(metrics_mean["acousticness"].round(3)), 
           float(metrics_mean["instrumentalness"].round(3)), 
           float(metrics_mean["speechiness"].round(3)))
    

@app.callback(
    Output('image_wc', 'src'), 
    [Input('song_genres', 'children')]
)
def make_word_cloud(song_genres):
    song_genres_dict = pd.Series(song_genres).value_counts().to_dict()

    wordcloud = WordCloud(background_color = "white", 
                          relative_scaling = 0.175,
                          scale =  1.5, 
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
     Output("sp_duration", "children")],
    [Input("spotify_default_song", "children"),
     Input("tracklist_data_clean", "children"),
     Input("tempo_graph", "clickData"),
     Input("key_graph", "clickData")]
)
def update_song(spotify_default_song, data, click_data_tempo, click_data_key):
    ctx = dash.callback_context
    
    data = pd.read_json(data)
    
    SPOTIFY_EMBED_URL_PREFIX = "https://open.spotify.com/embed/track/"
    SP_METRICS = ["energy", "danceability", "valence", "acousticness", "instrumentalness", "speechiness", "key", "mode", "tempo", "genres", "duration_ms"]
    
    if ctx.triggered[0]["prop_id"] == "spotify_default_song.children":
        song_clicked_name = spotify_default_song[0]
        song_clicked_id = spotify_default_song[1]
        
    else:
        clicked_data = ctx.triggered[0]["value"]["points"][0]["customdata"]
        song_clicked_name = clicked_data[0]
        song_clicked_id = clicked_data[-1]
    
    song_spotify_embed = SPOTIFY_EMBED_URL_PREFIX + song_clicked_id
    
    song_spotify_metrics = tuple(data[data["name"] == song_clicked_name][SP_METRICS].round(2).values.tolist()[0])
    
    return(song_clicked_name, song_spotify_embed, *song_spotify_metrics)













if __name__ == "__main__":
    app.run_server(debug = True, use_reloader = False)