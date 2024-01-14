import requests

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

dash.register_page(__name__, path='/dashboard')

container = dbc.Container(
    [   html.Div(id="hidden_div_for_redirect_callback"),
        html.P(""),
        html.P(""),
        dbc.Row(dbc.Col(html.H2("Dashboard"), width='auto'), justify="center"),
    
    ], id='main_container')

app.layout = container

if __name__ == "__main__":
    app.run_server()
