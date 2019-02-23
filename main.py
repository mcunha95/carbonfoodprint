import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import helper_data

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
all_keys = helper_data.get_food_category_and_item_dictionary()
slider_keys = helper_data.get_slider_box_keys()


def generateDropDown(categoryName):
    return dcc.Dropdown(
        id='dropdown-' + categoryName,
        options=[{'label': item, 'value': item} for item in helper_data.get_food_items('', '', categoryName)],
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


def generateSliderArea(categoryName):
    return html.Div(
        children=[generateSlider(item, categoryName) for item in helper_data.get_food_items('', '', categoryName)])


def generateCategorySection(categoryName):
    return html.Div(
        id='section-' + categoryName,
        children=[
            html.H1(categoryName),
            generateDropDown(categoryName),
            generateSliderArea(categoryName)
        ]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1('Carbon Food Print'),
    html.Img(
        src="https://media.licdn.com/dms/image/C5603AQG3ZEUy_W3qkQ/profile-displayphoto-shrink_200_200/0?e=1555545600&v=beta&t=BTyCpIJqrHQnKVIuNdaBgc6CwnYy6oYtfea_OT2qvbY",
        width=200,
        height=200),
    html.Div(children=[
        html.H3('What country do you want to check?'),
        dcc.Dropdown(
            id='country',
            options=helper_data.get_countries(),
            value=default_country
        )
    ]),
    html.Div(children=[
        html.H3('What age group are you in?'),
        dcc.Dropdown(
            id='age-group',
            options=helper_data.get_age_groups(default_country),
            value=default_age_group
        )
    ]),
    html.Div(children=[
        generateCategorySection(category)
        for category in helper_data.get_food_categories()
    ]),
    html.Div(id='live-graph')
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
    food_categories = helper_data.get_food_categories()
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
            



# country = 'Spain'
# foods = ['banana', 'avocado', 'fries', 'kapsalon']
# values_food_country = [1,5,2,4]
# values_food_person = [3,4,5,2]

# @app.callback(
#     Output(component_id='live-graph', component_property='children'),
#     [Input(component_id='id_input_1', component_property='value'),
#     Input(component_id='id_input_2', component_property='value')
#     ]
# )
# def update_output_div(input_value_1, input_value_2):
#     values_food_country[2] = input_value_1
#     values_food_country[1] = input_value_2
#     return html.Div(dcc.Graph(
#         id='country-person-graph',
#         figure={
#             'data': [
#                 {'x': foods, 'y': values_food_country, 'type': 'bar', 'name': country},
#                 {'x': foods, 'y': values_food_person, 'type': 'bar', 'name': 'You'},
#             ],
#             'layout': {
#                 'title': 'Comparison with your country'
#             }
#         }
#     ))


@app.callback(
    Output(component_id='age-group', component_property='options'),
    [Input(component_id='country', component_property='value')]
)
def update_age_groups(country):
    return helper_data.get_age_groups(country)


for category in helper_data.get_food_categories():
    @app.callback(
        Output('dropdown-'+category,'options'),
        [
            Input('age-group','value'),
            Input('country','value')
        ],
        [
            State('dropdown-'+category,'id')
        ]
    )
    def resetOptionsAgeChange(ageGroup,country, categoryId):
        categoryName=categoryId.split('-')[-1]
        return helper_data.get_dictionary_for_dash(helper_data.get_food_items(country, ageGroup, categoryName))
    
    @app.callback(
        Output('dropdown-'+category,'value'),
        [
            Input('dropdown-'+category,'options')
        ]
    )
    def clearSelections(CategoryOptions):
        return []


for category in helper_data.get_food_categories():
    for item in helper_data.get_food_items('', '', category):
        @app.callback(
            Output('slider-value-box-' + category + '-' + item, 'children'),
            [
                Input('slider-' + category + '-' + item, 'value')
            ]
        )
        def setValue(inputValue):
            return inputValue

for category in helper_data.get_food_categories():
    for item in helper_data.get_food_items('', '', category):
        @app.callback(
            Output('slider-container-' + category + '-' + item, 'style'),
            [
                Input('dropdown-' + category, 'value')
            ],
            [
                State('slider-container-' + category + '-' + item, 'id')
            ]
        )
        def hideSlider(optionsArray, itemID):
            itemName = itemID.split('-')[-1]
            if optionsArray is None:
                return {'display': 'none'}
            if itemName in optionsArray:
                return {'display': 'block'}
            return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)
