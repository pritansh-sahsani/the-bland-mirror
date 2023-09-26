import dash
from dash import dcc, html
from flask_login.utils import login_required
import plotly.express as px
import pandas as pd

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)


def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
    dash_app._favicon = ("logo.png")

    dash_app.layout = html.Div(
        children=[
            html.H1(children="Hello Dash", className="h1"),
            html.Div(
                children="""
            Dash: A web application framework for Python.
        """
            ),
            dcc.Graph(
                id="example-graph",
                className="container",
                figure=px.bar(df, x="Fruit", y="Amount", color="City", barmode="group"),
            ),
        ]
    )

    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app