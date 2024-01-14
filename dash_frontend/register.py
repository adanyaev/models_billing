import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import requests

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

dash.register_page(__name__, path='/login')

container = dbc.Container(
    [   html.Div(id="hidden_div_for_redirect_callback"),
        html.P(""),
        html.P(""),
        dbc.Row(dbc.Col(html.H2("Register"), width='auto'), justify="center"),
        html.P(""),
        html.P(""),
        dbc.Row(
            html.Div(
                [
                    html.P("Email"),
                    dbc.Input(id="email-input", type="text",),
                ]     
        )),
        html.P(""),
        dbc.Row(
            html.Div(
                [
                    html.P("Password"),
                    dbc.Input(id="password-input", type="password",),
                ]
        )),
        html.P(""),
        dbc.Row(
            html.Div(
                [
                    html.P("Repeat assword"),
                    dbc.Input(id="password-input-repeat", type="password",),
                ]
        )),
        html.P(""),
        dbc.Row([
            dbc.Col(dbc.Button("Register", color="primary", className="me-1", id='reg_button', n_clicks=0), width='auto'),
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
    Output(component_id='hidden_div_for_redirect_callback', component_property='children'),
    Input(component_id='reg_button', component_property='n_clicks'),
    [dash.dependencies.State('email-input', 'value'),
     dash.dependencies.State('password-input', 'value'),
     dash.dependencies.State('password-input-repeat', 'value')],
     prevent_initial_call=True
)
def register(n_clicks, email, password, password_repeat):
    if n_clicks and n_clicks > 0:
        if password != password_repeat:
            return "Passwords do not match", True, ""
        print(email)
        res = requests.post("http://127.0.0.1:8080/sign_up/", json={
            "email": str(email),
            "password": str(password)
            })
        if res.status_code == 200:
            return "", False, dcc.Location(pathname="/login", id="someid_doesnt_matter")
        return res.json()['detail'], True, ""
        
    else:
        raise dash.exceptions.PreventUpdate
    

if __name__ == "__main__":
    app.run_server()