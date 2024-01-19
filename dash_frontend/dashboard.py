import requests

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dash.register_page(__name__, path="/dashboard")


create_request_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Create inference request")),
        dbc.ModalBody(
            dbc.Container(
                [
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("SEQN"),
                                        dbc.Input(
                                            id="SEQN",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("RIAGENDR"),
                                        dbc.Input(
                                            id="RIAGENDR",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("PAQ605"),
                                        dbc.Input(
                                            id="PAQ605",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("BMXBMI"),
                                        dbc.Input(
                                            id="BMXBMI",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                        ],
                        justify="right",
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("LBXGLU"),
                                        dbc.Input(
                                            id="LBXGLU",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("DIQ010"),
                                        dbc.Input(
                                            id="DIQ010",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("LBXGLT"),
                                        dbc.Input(
                                            id="LBXGLT",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("LBXIN"),
                                        dbc.Input(
                                            id="LBXIN",
                                            placeholder="Enter float number...",
                                            type="number",
                                            step="any",
                                        ),
                                        dbc.FormText("Type something in the box above"),
                                    ]
                                ),
                                width=3,
                            ),
                        ],
                        justify="right",
                    ),
                    html.Br(),
                    dbc.Label("Choose model:"),
                    html.Br(),
                    dbc.Row(
                        dbc.Col(
                            dbc.Select(
                                id="select_model",
                                options=[
                                    {
                                        "label": "Disabled option",
                                        "value": "1",
                                        "disabled": True,
                                    },
                                ],
                            ),
                            width=5,
                        )
                    ),
                    html.Br(),
                    dbc.Button(
                        "Create request",
                        color="primary",
                        id="submit_request_butt",
                        className="me-1",
                        n_clicks=0,
                    ),
                    html.Br(),
                    html.Br(),
                    dbc.Alert(
                        "Hello! I am an alert",
                        id="create_request_alert",
                        color="danger",
                        dismissable=True,
                        is_open=False,
                    ),
                ]
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal",
    size="xl",
    is_open=False,
)


container = dbc.Container(
    [
        create_request_modal,
        html.Div(id="hidden_div_for_redirect_callback"),
        html.P(""),
        html.P(""),
        dbc.Row(dbc.Col(html.H2("Dashboard"), width="auto"), justify="center"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.H5("Hello", id="user_name"), width=2),
                dbc.Col(
                    [html.H5("Your balance:"), html.H4("Balance", id="user_balance")],
                    width=2,
                ),
            ],
            justify="center",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Show available models information",
                        id="collapse-button",
                        className="mb-3",
                        color="info",
                        n_clicks=0,
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Button(
                        "Create inference request", id="create_request_butt", n_clicks=0
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Button(
                        "Update info", color="success", id="reload_butt", n_clicks=0
                    ),
                    width="auto",
                ),
            ]
        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    "Models info", id="models_info", style={"white-space": "pre-wrap"}
                )
            ),
            id="collapse",
            is_open=False,
        ),
        html.Br(),
        html.H5("Inference requests"),
        html.Br(),
        dbc.Card(
            dbc.ListGroup(
                # [
                #     dbc.ListGroupItem("Item 1"),
                #     dbc.ListGroupItem("Item 2"),
                #     dbc.ListGroupItem("Item 3"),
                # ],
                flush=True, id='requests_table'
            ),
            style={"width": "60rem"},
        )
    ],
    id="main_container",
)

app.layout = container


@callback(
    Output(component_id="user_data", component_property="data"),
    Output(component_id="user_name", component_property="children"),
    Output(component_id="user_balance", component_property="children"),
    Output(component_id="models_info", component_property="children"),
    Output(component_id="select_model", component_property="options"),
    Output(component_id="requests_table", component_property="children"),
    Input("reload_butt", "n_clicks"),
    dash.dependencies.State(component_id="token", component_property="data"),
)
def fetch_user_info(n_clicks, token):
    res = requests.get(
        "http://backend:8080/my_user_info/",
        headers={"Authorization": f"Bearer {token}"},
    )
    res_models = requests.get(
        "http://backend:8080/available_models/",
        headers={"Authorization": f"Bearer {token}"},
    )
    res_requests = requests.get(
        "http://backend:8080/inf_requests/",
        headers={"Authorization": f"Bearer {token}"},
    )
    if res.status_code == 200 and res_models.status_code == 200 and res_requests.status_code == 200:
        user_data = res.json()
        models_data = res_models.json()
        requests_data = res_requests.json()
        models_description = ""
        select_options = []
        for model in models_data:
            for key in model:
                if key != "id":
                    models_description += f"{key}: {model[key]}\n"
            select_options.append(
                {
                    "label": f'{model["name"]}, price={model["price"]}',
                    "value": model["id"],
                }
            )
            models_description += "\n\n"

        list_items = []
        for request in requests_data:

            table_header = [
                html.Thead(html.Tr([html.Th("SEQN"), html.Th("RIAGENDR"), html.Th("PAQ605"), html.Th("BMXBMI"),
                                    html.Th("LBXGLU"), html.Th("DIQ010") ,html.Th("LBXGLT"), html.Th("LBXIN")]))
            ]
            row1 = html.Tr([html.Td(request['SEQN']), html.Td(request['RIAGENDR']), html.Td(request['PAQ605']), html.Td(request['BMXBMI']),
                            html.Td(request['LBXGLU']), html.Td(request['DIQ010']), html.Td(request['LBXGLT']), html.Td(request['LBXIN'])])
            table_body = [html.Tbody([row1])]
            table = dbc.Table(table_header + table_body, bordered=True)

            item = dbc.ListGroupItem([html.H5(f"Model name: {request['model']['name']}"),
                                      html.P(f"Request price: {request['cost']}"),
                                      table,
                                      html.P(f"Result: {request['inference_result']['value']}")
                                      ])
            list_items.append(item)
        
            
        return (
            user_data,
            f"Hello, {user_data['email']}",
            str(user_data["balance"]),
            models_description,
            select_options,
            list_items
        )

    return


@callback(
    Output("modal", "is_open", allow_duplicate=True),
    Output("reload_butt", "n_clicks"),
    Output(component_id="create_request_alert", component_property="children"),
    Output(component_id="create_request_alert", component_property="is_open"),
    Input("submit_request_butt", "n_clicks"),
    [   
        dash.dependencies.State("token", "data"),
        dash.dependencies.State("select_model", "value"),
        dash.dependencies.State("reload_butt", "n_clicks"),
        dash.dependencies.State("SEQN", "value"),
        dash.dependencies.State("RIAGENDR", "value"),
        dash.dependencies.State("PAQ605", "value"),
        dash.dependencies.State("BMXBMI", "value"),
        dash.dependencies.State("LBXGLU", "value"),
        dash.dependencies.State("DIQ010", "value"),
        dash.dependencies.State("LBXGLT", "value"),
        dash.dependencies.State("LBXIN", "value"),
    ],
    prevent_initial_call=True,
)
def submit_request(
    n_clicks,
    token,
    model_id,
    reload_n_clicks,
    SEQN,
    RIAGENDR,
    PAQ605,
    BMXBMI,
    LBXGLU,
    DIQ010,
    LBXGLT,
    LBXIN,
):
    if n_clicks and n_clicks > 0:
        res = requests.post(
            "http://backend:8080/infer_model/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "ml_model_id": model_id,
                "SEQN": SEQN,
                "RIAGENDR": RIAGENDR,
                "PAQ605": PAQ605,
                "BMXBMI": BMXBMI,
                "LBXGLU": LBXGLU,
                "DIQ010": DIQ010,
                "LBXGLT": LBXGLT,
                "LBXIN": LBXIN,
            },
        )
        if res.status_code == 200:
            response = res.json()
            return False, reload_n_clicks+1, "", False

        return True, reload_n_clicks, res.json()["detail"], True

    else:
        raise dash.exceptions.PreventUpdate


@callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    [dash.dependencies.State("collapse", "is_open")],
    prevent_initial_call=True,
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks and n_clicks > 0:
        return not is_open
    else:
        raise dash.exceptions.PreventUpdate


@callback(
    Output("modal", "is_open"),
    [Input("create_request_butt", "n_clicks"), Input("close", "n_clicks")],
    [dash.dependencies.State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server()
