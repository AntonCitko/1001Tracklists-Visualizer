import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_synthesizer import get_data
import pandas as pd
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from flask_caching import Cache
from wordcloud import WordCloud
import os

#%%

import dash
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html

from io import BytesIO

import pandas as pd
from wordcloud import WordCloud
import base64

#%%

# url = "https://www.1001tracklists.com/tracklist/2rskz669/jstjr-kill-the-noise-night-owl-radio-243-2020-04-11.html"

#url = "https://www.1001tracklists.com/tracklist/2vhlqun9/louis-the-child-alison-wonderland-night-owl-radio-236-2020-02-22.html"

url= "https://www.1001tracklists.com/tracklist/2bqc73r1/zeds-dead-circuitgrounds-edc-las-vegas-united-states-2019-05-19.html"

data = get_data(url)

#%%

def time_to_float(time):
    time_vals = time.split(":")[::-1]
    seconds = 0
    
    for i, time in enumerate(time_vals):
        seconds += int(time) * (60 ** i)
    
    return(seconds)

data["time"] = data["time"].replace(r'^\s*$', np.nan, regex=True)

data["time"] = data["time"].ffill()

data["time"] = data["time"].str.strip()

data["seconds"] = data["time"].apply(time_to_float)

song_genres = data["genres"].dropna().to_list()
song_genres = [genre for genre_list in song_genres for genre in genre_list.split(",") if genre]

data_missing = data[data["tempo"].isnull()]

data_clean = data.dropna(subset = ["tempo"])

#%%

data_tempo_mean = data_clean.groupby("seconds")["tempo"].mean()

#%%

song_genres_dict = pd.Series(song_genres).value_counts().to_dict()

wordcloud = WordCloud(background_color = "white", 
                      relative_scaling = 0.175,
                      scale =  1.5, 
                      repeat = True, 
                      max_words = 300,
                      min_font_size = 3).generate_from_frequencies(song_genres_dict)

image = wordcloud.to_image()

#%%

app = dash.Dash(__name__)

### FIGURE 1

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x = data_clean.seconds,
                y = data_clean.energy.rolling(3, min_periods = 1, center = True).mean(),
                name = "Energy",
                line_shape = "spline",
                line = dict(smoothing = 1.3,
                            color = "#542bc4")),
    secondary_y = False,
)

fig.add_trace(
    go.Scatter(x = data_clean.seconds,
                y = data_clean.danceability.rolling(3, min_periods = 1, center = True).mean(),
                name = "Danceability",
                line_shape = "spline",
                line = dict(smoothing = 1.3,
                            color = "#2b72c4")),
    secondary_y = False,
)

fig.add_trace(
    go.Scatter(x = data_tempo_mean.index,
                y = data_tempo_mean,
                name = "Tempo",
                line_shape = "spline",
                line = dict(width = 5,
                            color = "#2bc47d")),
    secondary_y = True
)


fig.add_trace(
    go.Scatter(x = data_clean.seconds,
                y = data_clean.tempo,
                name = "Song",
                mode = "markers",
                marker = dict(size = 10,
                              color = "#212120")),
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
        tickangle = 65
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
fig.update_yaxes(title_text="Spotify Value", secondary_y=False)
fig.update_yaxes(title_text="Beats per Minute", secondary_y=True)

### FIGURE 2


app.layout = html.Div(children = [
        html.H1(children = "1001Tracklists by the Numbers"),
        
        html.H2(children = "set"),
        
        dcc.Graph(
            id = "example3",
            figure = fig
            ),
        
        html.Div([
            html.Div([
                html.H3('Column 1'),
                html.Img(id = "image_wc"),
            ], className="six columns",
                style = dict(display = "inline-block", align = "left")),
    
            html.Div([
                html.H3('Column 2'),
                 dcc.Graph(
                     id = "example4",
                     figure = fig
                     )
            ], className="six columns",
                style = dict(width = "65%", display = "inline-block", align = "right"))
        ], className="row", 
            style = dict(display = "flex"))
    ])

@app.callback(dd.Output('image_wc', 'src'), [dd.Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    image.save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

if __name__ == "__main__":
    app.run_server(debug = False)