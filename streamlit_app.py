import streamlit as st
import csv
import pandas as pd
from itertools import islice
import pydeck as pdk
import numpy as np

# open csv file
rows = []
with open('./us_cities.csv', 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    #takes in first 100 datapoints
    for row in islice(csvreader, 100):
        rows.append(row)

coordinates = []
for row in rows:
    #places the coordinates at the front (wasnt working without this)
    fixedCoords = row[-2:] + row[:-2] 
    #changes coordinate values to floats
    fixedCoords[0] = float(fixedCoords[0])
    fixedCoords[1] = float(fixedCoords[1])
    
    #random number for height on map
    fixedCoords.append(np.random.rand() * 1000)

    coordinates.append(fixedCoords)

# create dataframe
df = pd.DataFrame(coordinates, columns=["lat", "lon", 'id', 'state_code', 'state_name', 'city_name', 'county_name', 'height'])
st.write(df)

#create pydeck chart
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=55.999722,
        longitude=-161.207778,
        zoom=7,
        pitch=50,
    ),
    layers=[
        #column layer with first 10 rows, elevation scale is larger than other one, diff color
        pdk.Layer(
            "ColumnLayer",
            data=df[:10],
            get_position=["lon", "lat"],
            get_elevation="height",
            elevation_scale=100,
            radius=5000,
            get_fill_color=[255, 0, 140],
            pickable=True,
        ),
        pdk.Layer(
            "ColumnLayer",
            data=df[:10],
            get_position=["lon", "lat"],
            get_elevation="height",
            elevation_scale=50,
            radius=5000,
            get_fill_color=[0, 255, 140],
            pickable=True,
        ),
        #rest of the 90 datapoints
        pdk.Layer(
            "ColumnLayer",
            data=df[10:],
            get_position=["lon", "lat"],
            get_elevation="height",
            elevation_scale=50,
            radius=5000,
            get_fill_color=[0, 255, 255],
            pickable=True,
        )
    ],
    #show tooltip
    tooltip={"html":"<b>Longitude: </b> {lon} <br /> "
                    "<b>Latitude: </b>{lat} <br /> "
                    "<b>State Code: </b>{state_code} <br /> "
                    "<b>State: </b>{state_name} <br /> "
                    "<b>City: </b>{city_name} <br /> "
                    "<b>County: </b>{county_name} <br /> "}
))