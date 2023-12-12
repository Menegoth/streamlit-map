import streamlit as st
import csv
import pandas as pd
from itertools import islice
import pydeck as pdk
import numpy as np

#slider to default how many cities are shown
states_slider = st.slider(label="How many datapoints?", min_value=1, max_value=27, value=27)
if states_slider:
    default = states_slider

# open csv file 
rows = []
with open('estados.csv', 'r', encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    #takes in specified datapoints
    for row in islice(csvreader, states_slider):
        rows.append(row)


for row in rows:
    # #random number for height on map
    row.append(np.random.rand() * 10000)

    # change coordinates to floats
    row[3] = float(row[3])
    row[4] = float(row[4])

# create dataframe
df = pd.DataFrame(rows, columns=["codigo_uf", "uf", 'nome', 'lat', 'lon', 'regiao', 'height'])

#create a city selector based on number of cities
states = []
for row in rows:
    states.append(row[2])
selectState = st.selectbox(label="Select a state", options=states)

#select a city to use for default pos
selectedState = 0
if selectState:
    selectedState = states.index(selectState)

#create pydeck chart
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=df.iloc[selectedState,3],
        longitude=df.iloc[selectedState,4 ],
        zoom=5,
        pitch=50,
    ),
    layers=[
        #two column layers with different elevation scalings
        pdk.Layer(
            "ColumnLayer",
            data=df,
            get_position=["lon", "lat"],
            get_elevation="height",
            elevation_scale=100,
            radius=50000,
            get_fill_color=[255, 0, 140],
            pickable=True,
        ),
        pdk.Layer(
            "ColumnLayer",
            data=df,
            get_position=["lon", "lat"],
            get_elevation="height",
            elevation_scale=50,
            radius=50000,
            get_fill_color=[0, 255, 140],
            pickable=True,
        )
    ],
    #show tooltip
    tooltip={"html":"<b>Longitude: </b> {lon} <br /> "
                    "<b>Latitude: </b>{lat} <br /> "
                    "<b>UF Code: </b>{uf} <br /> "
                    "<b>State: </b>{nome} <br /> "
                    "<b>Region: </b>{regiao} <br /> "}
))