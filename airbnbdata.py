# -*- coding: utf-8 -*-
"""airbnbdata.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z8dkH0TXCTJjzp6Wp_IS0zK9Tk0q2sml
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import gzip
import shutil
import matplotlib.font_manager as font_manager

"""Unzip the gz file"""

with gzip.open('/content/listings.csv.gz', 'rb') as f_in:
    with open('/content/listings.csv', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

"""Reading CSV file. Th etotal number of rows in listing is 44666"""

pd.set_option('precision', 4)
data = pd.read_csv('/content/listings.csv')

data.shape

data = data.drop(['id','listing_url','scrape_id','last_scraped','name','neighborhood_overview','picture_url','host_id','host_url','host_name',
                  'host_since','host_location','host_about','host_thumbnail_url','host_picture_url','host_listings_count',
                  'host_verifications','host_has_profile_pic','calendar_last_scraped','first_review','last_review',
                  'calculated_host_listings_count','calculated_host_listings_count_entire_homes','calculated_host_listings_count_private_rooms',
                  'calculated_host_listings_count_shared_rooms','license','bathrooms', 'calendar_updated', 'host_total_listings_count'], 
                 axis=1)

data.dtypes

"""Remove unwanted chracters from price. Convert price to float. Select properties with price more than 0"""

data['price'] = data['price'].str.replace('$', '')
data['price'] = data['price'].str.replace(',', '')
data["price"] = pd.to_numeric(data["price"], downcast="float")
data = data[data.price > 0]

data.isnull().sum().sort_values(ascending=False)

data = data[data.beds > 0]
data.loc[data['bedrooms'].isnull(), 'bedrooms'] = 1.0

data.describe()

data.head()

data['neighbourhood_group_cleansed'].unique()

labels = data.neighbourhood_group_cleansed.value_counts().index
colors = ['#008fd5','#fc4f30','#e5ae38','#6d904f','#8b8b8b']

shape = data.neighbourhood_group_cleansed.value_counts().values

plt.figure(figsize=(8,8))
plt.pie(shape, labels=shape, colors= colors, autopct = '%1.1f%%', startangle=90)
plt.legend(labels)
plt.title('Neighbourhood Group')
plt.show()

labels = data.room_type.value_counts().index

colors = ['#008fd5','#fc4f30','#e5ae38','#6d904f']

shape = data.room_type.value_counts().values

plt.figure(figsize=(8,8))
plt.bar(labels, shape, color=colors)
plt.title('Room type')
plt.show()

coord = data.loc[:,['longitude','latitude']]
coord.describe()

import folium
from folium.plugins import HeatMap
# convert to (n, 2) nd-array format for heatmap

map_folium = folium.Map([40.715076, -73.991180],zoom_start=11.4)

HeatMap(data[['latitude','longitude']].dropna(),radius=8,gradient={0.2:'blue',0.4:'purple',0.6:'orange',1.0:'red'}).add_to(map_folium)
display(map_folium)

data.host_response_time.unique()