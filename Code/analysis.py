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

# Read the census data into a Pandas DataFrame
file_path = Path("Data/sfo_neighborhoods_census_data.csv")
sfo_data = pd.read_csv(file_path, index_col="year")
sfo_data.head()

# Calculate the mean number of housing units per year (hint: use groupby) 
mean_units_per_year = sfo_data.groupby('year').mean()['housing_units']
mean_units_per_year

# Save the dataframe as a csv file
mean_units_per_year.to_csv(Path('units_per_year.csv'))

# Use the Pandas plot function to plot the average housing units per year.
# Note: You will need to manually adjust the y limit of the chart using the min and max values from above.
# Optional Challenge: Use the min, max, and std to scale the y limits of the chart
units_y = [mean_units_per_year.min() - mean_units_per_year.std(), mean_units_per_year.max() + mean_units_per_year.std()]
mean_units_per_year.plot.bar(
    xlabel = 'Years', 
    ylabel = 'Housing Units', 
    ylim = units_y, 
    title = 'Housing Units in San Francisco from 2010 to 2016')

# Calculate the average sale price per square foot and average gross rent
mean_gross_rent = sfo_data.groupby('year').mean()['gross_rent']
mean_gross_rent

mean_price_sqr_foot = sfo_data.groupby('year').mean()['sale_price_sqr_foot']
mean_price_sqr_foot

# Create two line charts, one to plot the average sale price per square foot and another for average montly rent

# Line chart for average sale price per square foot
mean_price_sqr_foot.plot.line(
    xlabel = 'Year', 
    ylabel = 'Price per SqFt', 
    title = 'Average Price per SqFt by Year')

# Line chart for average montly rent
mean_gross_rent.plot.line(
    xlabel = 'Year', 
    ylabel = 'Gross Rent', 
    title = 'Average Gross Rent by Year', 
    color = 'red')

# Group by year and neighborhood and then create a new dataframe of the mean values
mean_price_year_hood = sfo_data.groupby(['year', 'neighborhood']).mean()
mean_price_year_hood

# Use hvplot to create an interactive line chart of the average price per sq ft.
# The plot should have a dropdown selector for the neighborhood
avg_price = mean_price_year_hood['sale_price_sqr_foot'].hvplot.line(
    xlabel = 'Year', 
    ylabel = 'Avg Price/SqFt', 
    groupby = 'neighborhood', 
    title = 'Average Price per SqFt by Neighborhood')
avg_price

# Use hvplot to create an interactive line chart of the average monthly rent.
# The plot should have a dropdown selector for the neighborhood
avg_rent = mean_price_year_hood['gross_rent'].hvplot.line(
    xlabel = 'Year', 
    ylabel = 'Avg Gross Rent', 
    groupby = 'neighborhood', 
    title = 'Average Rent by Neighborhood')
avg_rent

# Getting the data from the top 10 expensive neighborhoods to own
top_10 = sfo_data.groupby('neighborhood').mean()['sale_price_sqr_foot'].sort_values(ascending = False).head(10)
top_10

# Plotting the data from the top 10 expensive neighborhoods
top_10_y = [top_10.min() - (top_10.std() / 2), top_10.max() + (top_10.std() / 2)]
top_10_plot = top_10.hvplot.bar(
    height = 450, 
    xlabel = 'Neighborhood', 
    ylabel = 'Avg. Sale Price per Square Foot', 
    rot = 90, ylim = top_10_y, 
    title = 'Top 10 Expensive Neighborhoods in SFO')
top_10_plot

# Fetch the previously generated DataFrame that was grouped by year and neighborhood
mean_price_year_hood

# Plot side-by-side comparison of average price per square foot versus average monthly rent by year with a dropdown selector for the neighborhood
comb_plot = mean_price_year_hood.hvplot.bar(
    height = 450, x = 'year', 
    y = ['gross_rent', 'sale_price_sqr_foot'], 
    stacked = False, 
    xlabel = 'Year', 
    ylabel = 'USD', 
    rot = 90, 
    groupby = 'neighborhood', 
    title = 'Average Rent by Neighborhood')
comb_plot

# Load neighborhoods coordinates data
map_data = pd.read_csv('Data/neighborhoods_coordinates.csv').set_index('Neighborhood')
map_data.head()

# Calculate the mean values for each neighborhood
sfo_mean = sfo_data.rename(str.title, axis = 'columns').groupby('Neighborhood').mean()
sfo_mean.head()

# Join the average values with the neighborhood locations
joined_data = pd.merge(map_data, sfo_mean, how = 'inner', on = 'Neighborhood')
joined_data.head()

# Fetch the data from all expensive neighborhoods per year.
top_10_par = sfo_data.groupby('neighborhood').mean().sort_values(by = 'sale_price_sqr_foot', ascending = False).head(10).reset_index()
top_10_par

# Parallel Categories Plot
par_cat = px.parallel_categories(top_10_par, color = 'sale_price_sqr_foot', width = 1200)
par_cat.show()
par_cat.write_image('Images/par_cat.png')

# Parallel Coordinates Plot
par_coor = px.parallel_coordinates(top_10_par, color = 'sale_price_sqr_foot', width = 1200)
par_coor.show()
par_coor.write_image('Images/par_coor.png')

# Sunburst Plot
expensive_neighborhoods = top_10_par['neighborhood']
expensive_neighborhoods

sunburst_data = sfo_data[sfo_data['neighborhood'].isin(expensive_neighborhoods)].reset_index()
sunburst_data.head()

sunburst = px.sunburst(
    sunburst_data,
    path = ['year', 'neighborhood'],
    values = 'sale_price_sqr_foot',
    color = 'gross_rent',
    color_continuous_scale = 'blues',
    height = 800,
    title = 'Cost Analysis of Most Expensive neighborhoods in San Francisco per Year')
sunburst.show()
sunburst.write_image('Images/sunburst.png')


