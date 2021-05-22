# imports
import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot
import hvplot.pandas
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

import warnings
warnings.filterwarnings('ignore')

# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("mapbox_api_key")
px.set_mapbox_access_token(map_box_api)

# Import the necessary CSVs to Pandas DataFrames
sfo_data = pd.read_csv('Data/sfo_neighborhoods_census_data.csv', index_col="year")
map_data = pd.read_csv('Data/neighborhoods_coordinates.csv').set_index('Neighborhood')

# Define Panel Visualization Functions
def housing_units_per_year():
    """Housing Units Per Year."""
    mean_units_per_year = sfo_data.groupby('year').mean()['housing_units']
    units_y = [mean_units_per_year.min() - (mean_units_per_year.std() / 2), mean_units_per_year.max() + (mean_units_per_year.std() / 2)]
    fig = px.bar(mean_units_per_year,
        range_y=units_y,
        color_discrete_map = {'housing_units' : 'green'},
        title = 'Housing Units in San Francisco from 2010 to 2016')
    return pn.Pane(fig)

def average_gross_rent():
    """Average Gross Rent in San Francisco Per Year."""
    mean_gross_rent = sfo_data.groupby('year').mean()['gross_rent']
    fig = px.line(mean_gross_rent, 
        color_discrete_map={'gross_rent':'turquoise'},
        title = 'Average Gross Rent by Year')
    return pn.Pane(fig)

def average_sales_price():
    """Average Sales Price Per Year."""
    mean_price_sqr_foot = sfo_data.groupby('year').mean()['sale_price_sqr_foot']
    fig = px.line(mean_price_sqr_foot,
        title = 'Average Price per SqFt by Year')
    return pn.Pane(fig)

def average_price_by_neighborhood():
    """Average Prices by Neighborhood."""
    mean_price_year_hood = sfo_data.groupby(['year', 'neighborhood']).mean()
    fig = mean_price_year_hood['sale_price_sqr_foot'].hvplot.line(
        xlabel = 'Year', 
        ylabel = 'Avg Price/SqFt', 
        groupby = 'neighborhood', 
        title = 'Average Price per SqFt by Neighborhood')
    return fig

def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""
    top_10 = sfo_data.groupby('neighborhood').mean()['sale_price_sqr_foot'].sort_values(ascending = False).head(10)
    top_10_y = [top_10.min() - (top_10.std() / 2), top_10.max() + (top_10.std() / 2)]
    fig = px.bar(top_10,
        range_y = top_10_y)
    return pn.Pane(fig)

def most_expensive_neighborhoods_rent_sales():
    """Comparison of Rent and Sales Prices of Most Expensive Neighborhoods."""
    mean_price_year_hood = sfo_data.groupby(['year', 'neighborhood']).mean()
    fig  = mean_price_year_hood.hvplot.bar(
        height = 450, x = 'year', 
        y = ['gross_rent', 'sale_price_sqr_foot'], 
        stacked = False, 
        xlabel = 'Year', 
        ylabel = 'USD', 
        rot = 90, 
        groupby = 'neighborhood', 
        title = 'Average Rent by Neighborhood')
    return fig
    
    
def parallel_coordinates():
    """Parallel Coordinates Plot."""
    top_10 = sfo_data.groupby('neighborhood').mean()['sale_price_sqr_foot'].sort_values(ascending = False).head(10)
    top_10_y = [top_10.min() - (top_10.std() / 2), top_10.max() + (top_10.std() / 2)]
    top_10_par = sfo_data.groupby('neighborhood').mean().sort_values(by = 'sale_price_sqr_foot', ascending = False).head(10).reset_index()
    fig = px.parallel_coordinates(top_10_par, color = 'sale_price_sqr_foot', width = 1200)
    return pn.Pane(fig)


def parallel_categories():
    """Parallel Categories Plot."""
    top_10 = sfo_data.groupby('neighborhood').mean()['sale_price_sqr_foot'].sort_values(ascending = False).head(10)
    top_10_y = [top_10.min() - (top_10.std() / 2), top_10.max() + (top_10.std() / 2)]
    top_10_par = sfo_data.groupby('neighborhood').mean().sort_values(by = 'sale_price_sqr_foot', ascending = False).head(10).reset_index()
    fig = px.parallel_categories(top_10_par, color = 'sale_price_sqr_foot', width = 1200)
    return pn.Pane(fig)


def neighborhood_map():
    """Neighborhood Map."""
    map_data = pd.read_csv('Data/neighborhoods_coordinates.csv').set_index('Neighborhood')
    sfo_mean = sfo_data.rename(str.title, axis = 'columns').groupby('Neighborhood').mean()
    joined_data = pd.merge(map_data, sfo_mean, how = 'inner', on = 'Neighborhood')
    fig = px.scatter_mapbox(
        joined_data,
        lat = 'Lat',
        lon = 'Lon',
        size = 'Sale_Price_Sqr_Foot',
        color = 'Gross_Rent',
        zoom = 11,
        title = 'Average Sale Price per SqFt and Gross Rent in San Francisco',
        height = 650,
        width = 1200)
    return pn.Pane(fig)

def sunburst():
    """Sunburst Plot."""
    top_10 = sfo_data.groupby('neighborhood').mean()['sale_price_sqr_foot'].sort_values(ascending = False).head(10)
    top_10_y = [top_10.min() - (top_10.std() / 2), top_10.max() + (top_10.std() / 2)]
    top_10_par = sfo_data.groupby('neighborhood').mean().sort_values(by = 'sale_price_sqr_foot', ascending = False).head(10).reset_index()
    expensive_neighborhoods = top_10_par['neighborhood']
    sunburst_data = sfo_data[sfo_data['neighborhood'].isin(expensive_neighborhoods)].reset_index()
    fig = px.sunburst(
        sunburst_data,
        path = ['year', 'neighborhood'],
        values = 'sale_price_sqr_foot',
        color = 'gross_rent',
        color_continuous_scale = 'blues',
        height = 800,
        title = 'Cost Analysis of Most Expensive neighborhoods in San Francisco per Year')
    return pn.Pane(fig)

# Create a Title for the Dashboard
title = '# PYTHONIC MONOPOLY DASHBOARD'

# Create a tab layout for the dashboard
avg_column = pn.Column(
    '## Average Prices',
    housing_units_per_year(),
    pn.Row(average_gross_rent(),
    average_sales_price()),
    )

top_10_column = pn.Column(
    '## Top 10 Most Expensive Neighborhoods',
    top_most_expensive_neighborhoods(),
    sunburst())

interactive_column = pn.Column(
    most_expensive_neighborhoods_rent_sales(),
    average_price_by_neighborhood())

map_column = pn.Column(
    '## Map of San Francisco Neighborhoods',
    neighborhood_map())

parallel_column = pn.Column(
    '## Parallel Comparison',
    parallel_categories(),
    parallel_coordinates())

# Create the dashboard
sfo_rental_dashboard = pn.Tabs(
    ('Average Prices', avg_column),
    ('Top 10', top_10_column),
    ('Map', map_column),
    ('Neighborhoods', interactive_column),
    ('Parralel Comparison', parallel_column))

# Serve the# dashboard
sfo_rental_dashboard.servable()



