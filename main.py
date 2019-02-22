import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import helper_data

def generateDropDown(categoryName):
    return dcc.Dropdown(
        id='dropdown-'+categoryName,
        options=[{'label':item,'value':item} for item in helper_data.getFoodsInCategory(categoryName)],
        multi=True
    )

def generateSlider(itemName,categoryName):
    print('slider-container-'+categoryName+'-'+itemName)
    return html.Div(
        id='slider-container-'+categoryName+'-'+itemName,
        children=[
            html.H5(itemName),
            html.H5(id='slider-value-box-'+ categoryName+'-'+itemName),
            dcc.Slider(
                id='slider-'+ categoryName+'-'+itemName,
                min=0,
                max=10,
                step=1,
                value=0,
            )
        ]
    )

def generateSliderArea(categoryName):
    return html.Div(children=[generateSlider(item,categoryName) for item in helper_data.getFoodsInCategory(categoryName)])

def generateCategorySection(categoryName):
    return html.Div(
                    id='section-'+categoryName,
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
            options=helper_data.getCountries(),
            value='Belgium'
        )
    ]),
    html.Div(children=[
        html.H3('What age group are you in?'),
        dcc.Dropdown(
            id='age-groups',
            options=helper_data.getAgeGroups(),
            value='Adults'
        )
    ]),
    html.Div(children=[
        generateCategorySection(category)
        for category in helper_data.getFoodCategoryNames()
    ])
])


for category in ['x','y','z']:
    for item in ['a','b','c']:
        @app.callback(
            Output('slider-value-box-'+category+'-'+item, 'children'),
            [
                Input('slider-'+category+'-'+item,'value')
            ]
        )
        def setValue(inputValue):
            return inputValue


for category in ['x','y','z']:
    for item in ['a','b','c']:
        @app.callback(
        Output('slider-container-'+category +'-'+item,'style'),
        [
            Input('dropdown-'+category,'value')
        ],
        [
            State('slider-container-'+category+'-'+item,'id')
        ]
    )
        def hideSlider(optionsArray,itemID):
            print(itemID.split('-'))
            itemName = itemID.split('-')[-1]
            if optionsArray is None:
                return {'display':'none'}
            if itemName in optionsArray:
                return {'display':'block'}
            return {'display':'none'}

if __name__ == '__main__':
    app.run_server(debug=True)