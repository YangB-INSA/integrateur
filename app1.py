import dash

import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

# Iris bar figure
def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Data
df = px.data.iris()

# Build App
app1 = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app1.layout = html.Div(
    [
        # entête 
        dbc.Row([

            dbc.Col([
                html.Div([
                    html.Img(src = app1.get_asset_url('insa.png'))
                ]),
            ], width=2, className = 'my-auto text-center'),

            dbc.Col([
                html.Div([
                    html.H2("French air traffic visualization"),
                    html.H6("Made by Axolotl"),
                ], className = 'text-center'),
            ], width=8, className = 'my-auto'),

            dbc.Col([
                html.Div([
                    html.Img(src = app1.get_asset_url('logo.png'))
                ]),
            ], width=2, className = 'my-auto text-center'),

        ]),

        # graphe 
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody(
                        [
                            html.H5('Options', className = 'card-title'),
                            dcc.Graph(
                                figure=px.bar(
                                    df, x="sepal_width", y="sepal_length", color="species"
                                ).update_layout(
                                    template='plotly_dark',
                                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                    paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                ),
                                config={
                                    'displayModeBar': False
                                }
                            ) 
                        ]
                    )
                ])
            ], width = 4),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('Options', className = 'card-title'),
                            dcc.Graph(
                                figure=px.bar(
                                    df, x="sepal_width", y="sepal_length", color="species"
                                ).update_layout(
                                    template='plotly_dark',
                                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                    paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                ),
                                config={
                                    'displayModeBar': False
                                }
                            ) 
                        ]
                    )
                )
            ], width = 8),
        ]),

        dbc.Row([

        ]),

    ], 
    className = 'bg-light',
    style={
        "display": "flex",
        "flex-direction": "column",
        'background-color':'black'
    }
)

# Run app and display result inline in the notebook
if __name__ == "__main__":
    app1.run_server(debug=True)