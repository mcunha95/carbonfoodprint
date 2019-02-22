import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
        html.H3(fruit_category),
        dcc.Dropdown(
            id='fruit-category',
            options=helper_data.get_food_items(default_country, default_age_group, fruit_category)
        )
    ]),
    html.Div(children=[
        html.H3(meat_category),
        dcc.Dropdown(
            id='meat-category',
            options=helper_data.get_food_items(default_country, default_age_group, meat_category)
        )
    ]),
    html.Div(children=[
        html.H3(vegetable_category),
        dcc.Dropdown(
            id='vegetable-category',
            options=helper_data.get_food_items(default_country, default_age_group, vegetable_category)
        )
    ]),
    html.Div(children=[
        html.H3(grain_category),
        dcc.Dropdown(
            id='grain-category',
            options=helper_data.get_food_items(default_country, default_age_group, grain_category)
        )
    ]),
    html.Div(children=[
        html.H3(oil_category),
        dcc.Dropdown(
            id='oil-category',
            options=helper_data.get_food_items(default_country, default_age_group, oil_category)
        )
    ]),
    html.Div(children=[
        html.H3(dairy_category),
        dcc.Dropdown(
            id='dairy-category',
            options=helper_data.get_food_items(default_country, default_age_group, dairy_category)
        )
    ]),
    html.Div(children=[
        html.H3(nut_seed_legume_category),
        dcc.Dropdown(
            id='nut-seed-legume-category',
            options=helper_data.get_food_items(default_country, default_age_group, nut_seed_legume_category)
        )
    ]),
    html.Div(children=[
        html.H3(other_category),
        dcc.Dropdown(
            id='other-category',
            options=helper_data.get_food_items(default_country, default_age_group, other_category)
        )
    ])
])


@app.callback(
    Output(component_id='age-group', component_property='options'),
    [Input(component_id='country', component_property='value')]
)
def update_age_groups(country):
    return helper_data.get_age_groups(country)


@app.callback(
    Output(component_id='fruit-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_fruit_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Fruit')


@app.callback(
    Output(component_id='meat-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_meat_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Meat')


@app.callback(
    Output(component_id='vegetable-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_vegetable_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Vegetable')


@app.callback(
    Output(component_id='grain-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_grain_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Grain')


@app.callback(
    Output(component_id='oil-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_oil_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Oil')


@app.callback(
    Output(component_id='dairy-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_dairy_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Dairy')


@app.callback(
    Output(component_id='nut-seed-legume-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_nut_seed_legume_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Nut/Seed/Legume')


@app.callback(
    Output(component_id='other-category', component_property='options'),
    [Input(component_id='country', component_property='value'),
     Input(component_id='age-group', component_property='value')]
)
def update_other_items(country, age_group):
    return helper_data.get_food_items(country, age_group, 'Other')


if __name__ == '__main__':
    app.run_server(debug=True)