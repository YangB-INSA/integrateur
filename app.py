# Import required libraries
import os
import pickle
import copy
import datetime as dt
import math

import requests
import pandas as pd
from flask import Flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go

# Load data
df = pd.read_csv('data/part-00000.csv',sep=';')
df.columns = ['Date','Hour','Manufacturer','Operator','Model','NumberPlanes']

df['Date'] = pd.to_datetime(df['Date'],format = '%d/%m/%Y')
df['dayOfWeek']=df['Date'].dt.day_name()

print(df)

#df_test = df.groupby([df['dayOfWeek']]).count()
#print(df_test)
#print(df.value_counts(['dayOfWeek']))
#print(df.groupby([df['dayOfWeek']]).sum().reset_index())


start_date = min(df['Date'])
end_date = max(df['Date']) 

# Operator option 
operator_options = df.Operator.unique()

#Manufacturer options
Manufacturer_options = df.Manufacturer.unique()

#test = df.groupby([df['Date']]).sum().reset_index()
#print(test)

# Create the app
app = dash.Dash(__name__)
server = app.server

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Img(
                    src=app.get_asset_url('insa.png'),
                    className='two columns',
                ),
                html.Div(
                    [
                        html.H3(
                            'Data Visualisation of the French Air Traffic',
                        ),
                        html.H6(
                            'Made by Axolotl',
                        )
                    ],
                    className='eight columns',
                    style = {'text-align':'center'},
                ),
                html.Img(
                    src=app.get_asset_url('logos.png'),
                    className="two columns",
                )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            'Filter by flight date :',
                            className="control_label"
                        ),   
                        dcc.DatePickerRange(
                            id='date_picker_range',
                            day_size=50,
                            display_format='DD-MM-YYYY',
                            min_date_allowed=start_date,
                            max_date_allowed=end_date + dt.timedelta(days=1),
                            start_date = start_date,
                            end_date=end_date,
                            className='dcc_control'
                        ),                  
                        html.H6(
                            'Filter by Operator:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='operator_status_selector',
                            options=[
                                {'label': 'All ', 'value': 'all'},
                                {'label': 'Active only ', 'value': 'active'},
                                {'label': 'Customize ', 'value': 'custom'}
                            ],
                            value='all',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),
                        dcc.Dropdown(
                            id='operator_dropdown',
                            options=[{'label': i, 'value': i} for i in df.Operator.unique()],
                            value= df.Operator.unique(),
                            multi=True,
                            style={ "overflow-y":"scroll", "max-height": "250px"},
                        ), 
                                
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                    
                        html.Div(
                            [
                                dcc.Graph(
                                    id='nb_flights_graph',
                                )
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='main_graph',
                        )
                    ],
                    className='pretty_container seven columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='individual_graph')
                    ],
                    className='pretty_container five columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='pie_graph')
                    ],
                    className='pretty_container seven columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='aggregate_graph')
                    ],
                    className='pretty_container five columns',
                ),
            ],
            className='row'
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)



# filter dataframe based on selected values

def filter_dataframe(df, operator_options, start_date, end_date):
    dff = df[df['Operator'].isin(operator_options)
          & (df['Date'] >= start_date)
          & (df['Date'] <= end_date)]
    print(dff)
    return dff

# Create callbacks

@app.callback(Output('nb_flights_graph', 'figure'),
              [Input('operator_dropdown', 'value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_main_figure(operator_selected, start_date,end_date):

    print('----------------------- First callback -----------------------')
    dff = filter_dataframe(df, operator_selected, start_date, end_date)
    df_graph = dff.groupby([dff['Date']]).sum().reset_index()
    print(df_graph)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_graph['Date'], y=df_graph['NumberPlanes'],
                                 mode='lines+markers',
                                 name='NumberPlanes'))
    fig.update_layout(title_text = "Number of flights per date")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="number of Flights")
    return fig


@app.callback(Output('main_graph', 'figure'),
              [Input('operator_dropdown', 'value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_weekday_figure(operator_selected, start_date,end_date):

    print('---------------- im in the second callback --------------------')
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dff = filter_dataframe(df, operator_selected, start_date, end_date)
    df_graph = dff.groupby([dff['dayOfWeek']]).sum().reset_index()
    print(df_graph)
    df_graph['dayOfWeek'] = pd.Categorical(df_graph['dayOfWeek'], categories= weekdays)
    df_graph = df_graph.sort_values('dayOfWeek')
    print(df_graph)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_graph['dayOfWeek'], y=df_graph['NumberPlanes'],
                                
                                 name='NumberPlanes'))
    fig.update_layout(title_text = "Number of flights for each day of the week")
    fig.update_xaxes(title_text="Day of Week")
    fig.update_yaxes(title_text="Number of flights")

    return fig

@app.callback(Output('individual_graph', 'figure'),
              [Input('operator_dropdown', 'value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_hour_figure(operator_selected, start_date,end_date):

    print('---------------- im in the third callback --------------------')
    dff = filter_dataframe(df, operator_selected, start_date, end_date)
    df_graph = dff.groupby([dff['Hour']]).sum().reset_index()
    print(df_graph)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_graph['Hour'], y=df_graph['NumberPlanes'], name='NumberPlanes'))
    fig.update_layout(title_text = "Number of flights for each hour of the day")
    fig.update_xaxes(title_text="Hour of the day")
    fig.update_yaxes(title_text="Number of flights")

    return fig


# Main
if __name__ == '__main__':
    app.server.run(debug=True,port = 50001)
