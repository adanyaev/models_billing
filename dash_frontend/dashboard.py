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
    Input(component_id="token", component_property="data"),
)
def fetch_user_info(token):
    res = requests.get(
        "http://127.0.0.1:8080/my_user_info/",
        headers={"Authorization": f"Bearer {token}"},
    )
    res_models = requests.get(
        "http://127.0.0.1:8080/available_models/",
        headers={"Authorization": f"Bearer {token}"},
    )
    if res.status_code == 200 and res_models.status_code == 200:
        user_data = res.json()
        models_data = res_models.json()
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

        return (
            user_data,
            f"Hello, {user_data['email']}",
            str(user_data["balance"]),
            models_description,
            select_options,
        )

    return


@callback(
    Output("modal", "is_open", allow_duplicate=True),
    Output(component_id="create_request_alert", component_property="children"),
    Output(component_id="create_request_alert", component_property="is_open"),
    Input("submit_request_butt", "n_clicks"),
    [
        dash.dependencies.State("token", "data"),
        dash.dependencies.State("select_model", "value"),
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
            "http://127.0.0.1:8080/infer_model/",
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
            return False, "", False

        return True, res.json()["detail"], True

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
