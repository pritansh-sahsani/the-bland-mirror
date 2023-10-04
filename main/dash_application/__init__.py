import dash
from dash import dcc, html
from flask_login.utils import login_required
import plotly.express as px
import pandas as pd
from main.models import PageViews


def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
    dash_app._favicon = ("logo.png")

    # Code for the UI
    def app_layout():
        pageviews = PageViews.query.order_by(PageViews.date.desc()).all()

        dates = [pageview.date for pageview in pageviews]
        count = [pageview.count for pageview in pageviews]

        pageviewdf = pd.DataFrame(
            {
                "Dates": dates,
                "Count": count,
            }
        )

        print("\nDF: \n", pageviewdf, "\n\n\n")
        return html.Div(
            className="container mt-4",
            children=[
                html.H1(children="Hello Dash", className="h1"),
                html.Div(
                    children="""
                Dash: A web application framework for Python.
            """
                ),
                html.Hr(className="mt-2"),
                dcc.Graph(id="page-views-graph", figure=px.bar(pageviewdf, x="Dates", y="Count", title="Post Views Per Day")),
            ]
        )
        
    # Define the layout of the Dash application
    dash_app.layout = app_layout

    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app