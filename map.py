import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


import plotly.plotly as py
import pandas as pd
import math

import helper_data

# Read the data.
df=pd.read_csv('https://raw.githubusercontent.com/mcunha95/CarbonFoodPrint/master/df/CleanFoodData.csv')
co2fp_df=pd.read_csv('https://raw.githubusercontent.com/mcunha95/CarbonFoodPrint/master/df/CO2Footprint.csv')
co2mean_df=pd.read_csv('https://raw.githubusercontent.com/mcunha95/CarbonFoodPrint/master/df/CO2_per_country_ageGroup.csv')

for col in df.columns:
    df[col] = df[col].astype(str)
################################################################################
# APP
################################################################################

def legend_map_func(filtered_df):
	age_group = filtered_df.ageGroup.unique()[0]
	countries_age_group = filtered_df.Country.unique()
	categories = co2fp_df.Category.unique()

	#INIZALIZATION DICTIONARY
	legend_map = {}
	for country in countries_age_group:
	    legend_map[country] = dict()
	    for category in categories:
	        legend_map[country][category]=0
	    legend_map[country]['Total']=0

	#POPULATION
	cond_age_group = df.Pop_Class==age_group
	for country in countries_age_group:
	    cond_country = df.Country==country
	    for id in df[cond_country&cond_age_group].FoodId:
	        cond_ID = co2fp_df.ID==pd.to_numeric(id)
	        category = co2fp_df[cond_ID].Category
	        cond_dfID = df.FoodId==id
	        value=float(df[cond_country&cond_age_group&cond_dfID].Mean.values[0])
	        legend_map[country][category.values[0]]+=value
	        legend_map[country]['Total']+=value

	#NORMALIZATION
	for key, value in legend_map.items():
	    total = legend_map[key]['Total']
	    for key1, value1 in value.items():
	        legend_map[key][key1] = value1/total
	return legend_map

def euro_map(filtered_df):
	#scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'], [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
	
	legend_map = legend_map_func(filtered_df)
	txt = []
	for country in filtered_df['Country'].values:
		txtbycountry = ""
		for key1,value1 in legend_map[country].items():
			if key1 != 'Total':
				txtbycountry += " "+key1+": "+str(round(value1*100,2))+ '%<br>'
		txt.append(txtbycountry)
	filtered_df['text'] = txt#filtered_df['state'] + '<br>' +'Beef '+filtered_df['beef']+' Dairy '+filtered_df['dairy']+'<br>'+'Fruits '+filtered_df['total fruits']+' Veggies ' + filtered_df['total veggies']+'<br>'+'Wheat '+filtered_df['wheat']+' Corn '+filtered_df['corn']

	colorscale="Cividis"#YlOrRd,Portland,Hot,Electric,Viridis,Cividis.
	data = [ dict(
	        type='choropleth',
	        colorscale = colorscale,
	        autocolorscale = False,
	        locations = filtered_df['Country'],
	        z = filtered_df['Mean_CO2.g'].astype(float),
	        locationmode = 'country names',
	        text = filtered_df['text'],
	        marker = dict(
	            line = dict (
	                color = 'rgb(255,255,255)',
	                width = 1
	            ) ),
	        colorbar = dict(
	            title = "grams of CO2/day")
	        ) ]

	layout = dict(
		    autosize=False,
		    width=1000,
    		height=1000,
	        title = 'Avg Carbon Footprint Country Map',
	        geo = dict(
	            scope='europe',
	            projection=dict( type='Orthographic' ),
	            ),
	        )
	return {"data":data,"layout":layout}

################################################################################
# APP INITIALIZATION
################################################################################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "CarbonFoodPrint"

################################################################################
# LAYOUT
################################################################################
app.layout = html.Div(children=[
    html.Div([
        # Column: Map
        dcc.Graph(id="euro-map")
    ], className="row"),
	# Row: Filter 
    html.Div(children=[
        html.H4('What age group are you in?'),
        dcc.Dropdown(
            id='age-groups-map',
            options=helper_data.getAgeGroups(),
            value='Adults'
        )
    ]),
])

@app.callback(
    Output('euro-map', 'figure'),
    [Input('age-groups-map', 'value')]
)
def filter_euro_map(age_group):
	cond_age_group = co2mean_df['ageGroup']==age_group
	cond_non_cero = co2mean_df['Mean_CO2.g']!=0

	return euro_map(co2mean_df[(cond_age_group & cond_non_cero)])

if __name__ == '__main__':
    app.run_server(debug=True)