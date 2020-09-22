#Thanatip Chaiananporn 6030812921

import streamlit as st
import geopandas as gp
import pydeck as pdk
import altair as alt
import pandas as pd
import numpy as np
import folium as fo
from streamlit_folium import folium_static

st.title('Geospatial Data Science HW4: Streamlit with Folium (Data Tracking) \n (Thanatip Chaiananporn Student ID:6030812921)')

st.markdown("""- This site provided 5 days data from 01/01/2019 to 05/01/2019.""")
st.markdown("""- Please choose the date.""")

###Import Data URL###

df = ''
date = st.selectbox('Select Date',range(1,6),0)
if date == 1:
    df = pd.read_csv('https://raw.githubusercontent.com/Tibxch/steamlit/master/20190101.csv')
elif date == 2:
    df = pd.read_csv('https://raw.githubusercontent.com/Tibxch/steamlit/master/20190102.csv')
elif date == 3:
    df = pd.read_csv('https://raw.githubusercontent.com/Tibxch/steamlit/master/20190103.csv')
elif date == 4:
    df = pd.read_csv('https://raw.githubusercontent.com/Tibxch/steamlit/master/20190104.csv')
elif date == 5:
    df = pd.read_csv('https://raw.githubusercontent.com/Tibxch/steamlit/master/20190105.csv')

###Raw Data Visualization###
  
if st.checkbox("Show raw data", False):
    st.subheader('Raw Data')
    st.write(df)
    
#### GEOMETRY ###

crs = "EPSG:4326"
geometry = gp.points_from_xy(df.lonstartl, df.latstartl)
geo_df  = gp.GeoDataFrame(df,crs=crs,geometry=geometry)

### 3 Hours ####

hours_3 = st.slider("Hour of interest (Every 3 hours)",0,23,step=3)
data = geo_df
data["timestart"] = pd.to_datetime(data["timestart"])
    

### MAP ###

st.subheader("Map show data Picked up at %i:00" % (hours_3))
st.markdown(""" This map will show you only data of Picked up.""")
long = 100.5018 #longitude of BKK
lat = 13.7563 #latitude of BKK
station_map = fo.Map(
	location = [lat, long], 
	zoom_start = 10)

lat = list(geo_df.latstartl)
long = list(geo_df.lonstartl)
timestart = list(data.timestart)
ID = list(geo_df.ID)

for lat, lng,tstart,ID in zip(lat, long,timestart,ID):   ############
    if data.timestart[ID].hour == hours_3 and data.timestart[ID].year != 2018:
        fo.Marker(
            location = [lat, lng],
            popup = ['ID: ' + str(ID), lat, lng, tstart],
            icon = fo.Icon(color='blue', icon='map-marker')
        ).add_to(station_map)

folium_static(station_map)

#### GEO DATA ###

st.subheader("Geo data (Picked up) %i:00" % (hours_3))
st.markdown(""" This Geo data will show you only data of Picked up.""")
midpoint = (np.average(lat), np.average(long))
data = data[data["timestart"].dt.hour == hours_3]

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 12,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data = data,
            get_position = ['lonstartl', 'latstartl'],
            radius = 100,
            elevation_scale = 4,
            elevation_range = [0, 760],
            pickable = True,
            extruded = True,
        ),
    ],
))


##### GRAPH ####
st.subheader("Breakdown (Picked up) by minute %i:00" % (hours_3))
st.markdown(""" This graph will show you only data of Picked up.""")
filtered = data[
    (data["timestart"].dt.hour >= hours_3) & (data["timestart"].dt.hour < (hours_3 + 1))
]
hist = np.histogram(filtered["timestart"].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)
