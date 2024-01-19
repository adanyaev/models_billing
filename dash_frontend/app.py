from dash import Dash, dcc, html, Input, Output, callback
from dash_frontend import login, register, dashboard
import dash_bootstrap_components as dbc


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='token', storage_type='session'),
    dcc.Store(id='user_data', storage_type='session'),


    html.Div(id='page-content')
    
])


@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return login.container
    elif pathname == '/login':
        return login.container
    elif pathname == '/register':
        return register.container
    elif pathname == '/dashboard':
        return dashboard.container
    else:
        return '404'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8050", debug=False)
