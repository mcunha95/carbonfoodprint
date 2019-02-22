import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import helper_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1('Carbon Food Print'),
    html.Img(
        src="https://media.licdn.com/dms/image/C5603AQG3ZEUy_W3qkQ/profile-displayphoto-shrink_200_200/0?e=1555545600&v=beta&t=BTyCpIJqrHQnKVIuNdaBgc6CwnYy6oYtfea_OT2qvbY",
        width=200,
        height=200),
    html.Div(children=[
        html.H3('What age group are you in?'),
        dcc.Dropdown(
            id='age-groups',
            options=helper_data.getAgeGroups(),
            value='Adults'
        )
    ]),
    dcc.Dropdown(
            id='food-categories',
            options=helper_data.getFoodCategories(),
            value='')
])

if __name__ == '__main__':
    app.run_server(debug=True)