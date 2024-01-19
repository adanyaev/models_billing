import requests

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

dash.register_page(__name__, path='/login')

container = dbc.Container(
    [   html.Div(id="hidden_div_for_redirect_callback"),
        html.P(""),
        html.P(""),
        dbc.Row(dbc.Col(html.H2("Login"), width='auto'), justify="center"),
        html.P(""),
        html.P(""),
        dbc.Row(
            html.Div(
                [
                    dbc.Label("Email"),
                    dbc.Input(id="email-input", type="text",),
                ]
        )),
        html.P(""),
        dbc.Row(
            html.Div(
                [
                    dbc.Label("Password"),
                    dbc.Input(id="password-input", type="password",),
                ]
        )),
        html.P(""),
        dbc.Row([
            dbc.Col(dbc.Button("Login", color="primary", className="me-1", id='log_button'), width='auto'),
            dbc.Col(dbc.Button("Register", outline=True, color="primary", className="me-1", id='reg_button', n_clicks=0), width='auto'),
        ], align='left'),
        html.Br(),
        dbc.Alert(
            "Hello! I am an alert",
            id="alert-fade",
            color="danger",
            dismissable=True,
            is_open=False,
        ),
    
    ], id='main_container')

app.layout = container

@callback(
    Output(component_id='alert-fade', component_property='children', allow_duplicate=True),
    Output(component_id='alert-fade', component_property='is_open', allow_duplicate=True),
    Output(component_id='token', component_property='data', allow_duplicate=True),
    Output(component_id='hidden_div_for_redirect_callback', component_property='children', allow_duplicate=True),
    Input(component_id='log_button', component_property='n_clicks'),
    [dash.dependencies.State('email-input', 'value'),
     dash.dependencies.State('password-input', 'value')], 
     prevent_initial_call=True
)
def login(n_clicks, email, password):
    if n_clicks and n_clicks > 0:
        res = requests.post("http://backend:8080/sign_in/", json={
            "email": str(email),
            "password": str(password)
            })
        if res.status_code == 200:
            return "", False, res.json()['access_token'], dcc.Location(pathname="/dashboard", id="someid_doesnt_matter")
        return res.json()['detail'], True, None, ""
        
    else:
        raise dash.exceptions.PreventUpdate
    

@callback(
    Output(component_id='hidden_div_for_redirect_callback', component_property='children', allow_duplicate=True),
    Input(component_id='reg_button', component_property='n_clicks'),
    prevent_initial_call=True
)
def register(n_clicks):
    if n_clicks and n_clicks > 0:
        return dcc.Location(pathname="/register", id="someid_doesnt_matter")
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server()