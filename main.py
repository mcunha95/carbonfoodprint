import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import helper_data
import dash_daq as daq

default_country = 'Belgium'
default_age_group = 'Adults'

fruit_category = 'Fruit'
meat_category = 'Meat'
vegetable_category = 'Vegetable'
grain_category = 'Grain'
oil_category = 'Oil'
dairy_category = 'Dairy'
nut_seed_legume_category = 'Nut/Seed/Legume'
other_category = 'Other'

food_categories = helper_data.get_food_categories()
all_keys = helper_data.get_food_category_and_item_dictionary()
slider_keys = helper_data.get_slider_box_keys()


# Read the data.
df = pd.read_csv('df/CleanFoodData.csv')
co2fp_df = pd.read_csv('df/CO2Footprint.csv')
co2mean_df = pd.read_csv('df/CO2_per_country_ageGroup.csv')
################################################################################
# MAP
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
            width='auto',
            height=500,
            title = 'Avg Carbon Footprint Country Map',
            geo = dict(
                scope='europe',
                projection=dict( type='Orthographic' ),
                ),
            )
    return {"data":data,"layout":layout}

################################################################################
################################################################################



################################################################################
# RUSHIL:
################################################################################

def generateDropDown(categoryName, food_items_only_per_category):
    return dcc.Dropdown(
        id='dropdown-' + categoryName,
        options=[{'label': item, 'value': item} for item in food_items_only_per_category],
        multi=True
    )


def generateSlider(itemName, categoryName):
    return html.Div(
        id='slider-container-' + categoryName + '-' + itemName,
        children=[
            html.H5(itemName),
            html.H5(id='slider-value-box-' + categoryName + '-' + itemName),
            dcc.Slider(
                id='slider-' + categoryName + '-' + itemName,
                min=0,
                max=10,
                step=1,
                value=0,
            )
        ]
    )


def generateSliderArea(categoryName, food_items_only_per_category):
    return html.Div(
        children=[generateSlider(item, categoryName) for item in food_items_only_per_category],
            style={'marginLeft': 30, 'marginRight': 30, 'width': '200px'})


def generateCategorySection(categoryName):
    food_items_only_per_category = helper_data.get_food_items_only_per_category(categoryName)
    return html.Div(
        id='section-' + categoryName,
        children=[
            html.H3(categoryName),
            generateDropDown(categoryName, food_items_only_per_category),
            generateSliderArea(categoryName, food_items_only_per_category)
        ], style={'marginLeft': 30, 'marginRight': 30}
    )


################################################################################
################################################################################



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Bootstrap CSS
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})


app.layout = html.Div(children=[
    #Row 1
    html.Div([
        html.Img(
        src="http://www.greeneatz.com/wp-content/uploads/2013/01/foods-carbon-footprint.jpg",
        width='auto',
        height='auto',
        className = "two columns"),
        html.H1('My Carbon Food Print',  style={'color': 'white', 'fontSize': 30}, className = "ten columns")
    ], className = "row", style={'backgroundColor':'#8EB640'}),

    #Tabs
    html.Div([
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[

        	################################################################################
            #Tab one
            ################################################################################

            dcc.Tab(label='Data', children = [
                        html.Div(children=[
                            html.H3('What country do you want to check?',
                                style={'marginLeft': 30, 'marginRight': 30, 'marginTop': 10}),
                            dcc.Dropdown(
                                id='country',
                                options=helper_data.get_countries(),
                                value=default_country,
                                style={'marginLeft': 30, 'marginRight': 30, 'width': '200px'}
                            )
                        ]),
                        html.Div(children=[
                            html.H3('What age group are you in?',
                                style={'marginLeft': 30, 'marginRight': 30}),
                            dcc.Dropdown(
                                id='age-group',
                                options=helper_data.get_age_groups(default_country),
                                value=default_age_group,
                                style={'marginLeft': 30, 'marginRight': 30, 'width': '200px'}
                            )
                        ]),
                        html.Div(children=[
                            generateCategorySection(category)
                            for category in food_categories
                        ]),
                        html.Div(id='my-carbon-food-print-div'),
                        html.Div(id='live-graph')
                ], className = "six columns"),

            ################################################################################
            #Tab two
            ################################################################################

            dcc.Tab(label='Graph', children =[

                    #Code in tab
                    html.Div([
                        # Column: Map
                        dcc.Graph(id="euro-map")
                    ], className="row"),
                    # Row: Filter
                    html.Div(children=[
                        html.H4('What age group are you in?'),
                        dcc.Dropdown(
                            id='age-groups-map',
                            options=helper_data.get_all_age_groups(),
                            value='Adults'
                        )
                    ]),
                    #Code in tab

                ], className = "six columns"),
            #End tabs

        ]),
    ], className="row"),

])

@app.callback(
    Output(component_id='live-graph',component_property='children'),
    [
        Input('country','value'),
        Input('age-group','value')
    ]+
    [
        Input(sliderValueId, 'value') for sliderValueId in slider_keys
    ]
)
def generateGraph(country, ageGroup, *args):
    newDict = {}
    i = 0
    for category in food_categories:
        newDict[category] = {}
        for item in all_keys[category]:
            newDict[category][item]=args[i]
            i+=1
    # from here we need to take the new dict and generate the graphs
    dataArrays=helper_data.generate_data_arrays(newDict)
    return html.Div(children=[
        dcc.Graph(
            id='country-person-graph-agg',
            figure={
                'data': [
                    {'x': dataArrays['your_food_choices_all_categories'], 'y': dataArrays['your_food_choices_aggregated_emissions'], 'type': 'bar', 'name': 'You'},
                ],
                'layout': {
                    'title': 'Comparison with your country'
                }
            }
        ),
        dcc.Graph(
            id='country-person-graph',
            figure={
                'data': [
                    {'x': dataArrays['your_food_choices_item'], 'y': dataArrays['your_food_choices_emissions'], 'type': 'bar', 'name': 'You'},
                ],
                'layout': {
                    'title': 'Comparison with your country'
                }
            }
        )
        ])


@app.callback(
    Output('euro-map', 'figure'),
    [Input('age-groups-map', 'value')]
)
def filter_euro_map(age_group):
    cond_age_group = co2mean_df['ageGroup'] == age_group
    cond_non_cero = co2mean_df['Mean_CO2.g'] != 0
    return euro_map(co2mean_df[(cond_age_group & cond_non_cero)])

@app.callback(
    Output(component_id='age-group', component_property='options'),
    [Input(component_id='country', component_property='value')]
)
def update_age_groups(country):
    return helper_data.get_age_groups(country)


for category in food_categories:
    @app.callback(
        Output('dropdown-' + category, 'options'),
        [Input('age-group', 'value'),
        Input('country', 'value')],
        [State('dropdown-' + category, 'id')]
    )
    def resetOptionsAgeChange(ageGroup, country, categoryId):
        categoryName = categoryId.split('-')[-1]
        return helper_data.get_food_items(country, ageGroup, categoryName)


    @app.callback(
        Output('dropdown-' + category, 'value'),
        [Input('dropdown-' + category, 'options')]
    )
    def clearSelections(CategoryOptions):
        return []

for category in food_categories:
    for item in helper_data.get_food_items_only_per_category(category):
        @app.callback(
            Output('slider-value-box-' + category + '-' + item, 'children'),
            [Input('slider-' + category + '-' + item, 'value')]
        )
        def setValue(inputValue):
            return inputValue

for category in food_categories:
    for item in helper_data.get_food_items_only_per_category(category):
        @app.callback(
            Output('slider-container-' + category + '-' + item, 'style'),
            [Input('dropdown-' + category, 'value')],
            [State('slider-container-' + category + '-' + item, 'id')]
        )
        def hideSlider(optionsArray, itemID):
            itemName = itemID.split('-')[-1]
            if optionsArray is None:
                return {'display': 'none'}
            if itemName in optionsArray:
                return {'display': 'block'}
            return {'display': 'none'}


@app.callback(
    Output(component_id='my-carbon-food-print-div', component_property='children'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]+
    [Input(sliderValueId, 'value') for sliderValueId in slider_keys]
)
def get_my_carbon_food_print(country, age_group, *args):
    newDict = {}
    i = 0
    for category in food_categories:
        newDict[category] = {}
        for item in all_keys[category]:
            newDict[category][item] = args[i]
            i += 1
    my_carbon_food_print = helper_data.calculate_my_carbon_food_print(newDict)
    country_food_print = helper_data.get_carbon_food_print_for_country(country, age_group)
    return html.Div([
        html.Div([
            daq.Gauge(
                id='my-gauge',
                label='Your CO2 food print',
                max=100000,
                value=my_carbon_food_print,
                min=0)
        ], className="six columns"),
        html.Div([
            daq.Gauge(
                id='country-gauge',
                label=country + ' ' + age_group.lower() + ' CO2 food print',
                max=100000,
                value=country_food_print,
                min=0)
        ], className="six columns")
    ], className="row")


if __name__ == '__main__':
    app.run_server(debug=True)