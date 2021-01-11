# Import required libraries

import datetime as dt
import pandas as pd
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go

# Load data

#for local use
#df = pd.read_csv('data/data-plane.csv', sep='\t', header = None, error_bad_lines=False)

#for VM use 
df = pd.read_csv('/var/lib/jenkins/workspace/Microservice_Analyse/src/app/out/data-plane.csv', sep='\t', header = None, error_bad_lines=False)

# Some cleaning and edit on the dataset 
df = df.drop(df.columns[[0]], axis=1)
df.columns = ['Date','Hour','Manufacturer','Model','Operator','NumberFlights']
df['Date'] = pd.to_datetime(df['Date'])
df['DayOfWeek']=df['Date'].dt.day_name()
df['WeekNumber']=df['Date'].dt.week
df['Hour'] = pd.to_numeric(df['Hour'], errors = 'coerce')

# Range of the calendar
start_date = min(df['Date'])
end_date = max(df['Date']) 

# Operator option 
operator_options = df.Operator.unique()

#Manufacturer options
Manufacturer_options = df.Manufacturer.unique()

# Day Of Week options
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Create the app
app = dash.Dash(__name__)
server = app.server

# Create app layout
app.layout = html.Div(
    [
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
                            'Made by Axolotl Team',
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
                            'Filter by day of the week:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='day_selector',
                            options=[
                                {'label': 'All', 'value': 'all'},
                                {'label': 'Customized ', 'value': 'customized'},
                                {'label': 'None ', 'value': 'none'},
                            ],
                            value='all',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),

                        dcc.Dropdown(
                            id='day_dropdown',
                            options=[{'label': i, 'value': i} for i in weekdays],
                            value= weekdays,
                            multi=True,
                        ),                   
                        html.H6(
                            'Filter by Operator:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='operator_selector',
                            options=[
                                {'label': 'All', 'value': 'all'},
                                {'label': 'Customized ', 'value': 'customized'},
                                {'label': 'None ', 'value': 'none'},
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
                                html.Div(
                                    [
                                        html.H6(
                                            id="nb_operator",
                                            className="info_text"
                                        ),
                                        html.P("No. of operators"),
                                    ],                       
                                    className="pretty_container four columns",
                                    style = {'text-align':'center'}
                                ),

                                html.Div(
                                    [
                                        html.H6(
                                            id="nb_flights",
                                            className="info_text"
                                        ),
                                        html.P("No. of flights"),
                                    ],
                                    className="pretty_container four columns",
                                    style = {'text-align':'center'}
                                ),

                                html.Div(
                                    [
                                        html.H6(
                                            id="nb_days",
                                            className="info_text"
                                        ),
                                        html.P("No. of days"),
                                    ],
                                    className="pretty_container four columns",
                                    style = {'text-align':'center'}
                                ),
                                         
                            ],
                            id="infoContainer",
                            className="row",
                            style = {'display':'flex', 'align-items': 'center'}
                        ), 
                        html.Div(
                            [
                                dcc.Graph(
                                    id='total_graph',
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
                            id='week_graph',
                        )
                    ],
                    className='pretty_container seven columns',
                ),
                html.Div(
                    [ 
                        
                        dcc.Graph(
                            id='hour_graph'
                            )
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
                        dcc.Graph(id='weekday_graph')
                    ],
                    className='pretty_container four columns',
                ),
                html.Div(
                    [
                        html.H4(
                            'Operators of the french air traffic',
                            className = 'title',
                        ),
                        dash_table.DataTable(
                            id='data_table',
                            columns=[
                                {"name": i, "id": i} for i in ['Operator','Total No. of flights','Most used aircraft','Favorite manufacturer']
                            ],
                            page_current=0,
                            page_action='native',
                            page_size=10,
                        )
                    ],
                    className='pretty_container eight columns',
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

def filter_dataframe(df, operator_options, dayofweek, start_date, end_date):
    dff = df[df['Operator'].isin(operator_options)
          & (df['DayOfWeek']).isin(dayofweek)
          & (df['Date'] >= start_date)
          & (df['Date'] <= end_date)]
    return dff

# Create callbacks

# make texts above main_figure
@app.callback(Output('nb_operator', 'children'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def update_operator_text(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    nb_operators = dff.Operator.unique().shape
    return nb_operators

@app.callback(Output('nb_flights', 'children'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def update_flights_text(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    nb_flights = dff['NumberFlights'].sum()
    return nb_flights

@app.callback(Output('nb_days', 'children'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def update_day_text(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    nb = dff.Date.unique().shape
    return nb

# Radio -> multi
@app.callback(Output('day_dropdown', 'value'),
              [Input('day_selector', 'value')],
              [State('day_dropdown','value')])
def day_value(selector,prev_value):
    if selector == 'all':
        return weekdays
    elif selector == 'none':
        return []
    else:
        return prev_value


# Radio -> multi
@app.callback(Output('operator_dropdown', 'value'),
              [Input('operator_selector', 'value')],
              [State('operator_dropdown','value')])
def operator_value(selector,prev_value):
    if selector == 'all':
        return operator_options
    elif selector == 'none':
        return []
    else:
        return prev_value

# Radio -> multi
@app.callback(Output('day_selector', 'value'),
              [Input('day_dropdown', 'value')])
def day_radio_value(dropdown):
    if dropdown == weekdays:
        return 'all'
    elif dropdown == []:
        return 'none'
    else:
        return 'customized'

# Radio -> multi
@app.callback(Output('operator_selector', 'value'),
              [Input('operator_dropdown', 'value')])
def operator_radio_value(dropdown):
    if dropdown == operator_options:
        return 'all'
    elif dropdown == []:
        return 'none'
    else:
        return 'customized'

# callback for main_figure
@app.callback(Output('total_graph', 'figure'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_main_figure(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    df_graph = dff.groupby([dff['Date']]).sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_graph['Date'], y=df_graph['NumberFlights'],mode='lines', name='NumberFlights'))
    fig.update_layout(title_text = "Number of flights per date", 
                        title_x=0.5,
                        title_font_size=18, 
                        template='none',
                        paper_bgcolor='#fafafa',
                        plot_bgcolor='#fafafa',
                        margin=dict(l=50, r=40, t=70, b=70)
                        )
    fig.update_traces(marker_color= 'tomato')
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="number of Flights")
    return fig


# callback for week_figure
@app.callback(Output('week_graph', 'figure'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_week_figure(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    df_graph = dff.groupby([dff['WeekNumber']]).sum().reset_index()
    fig = px.bar(df_graph, x='WeekNumber', y='NumberFlights', text='NumberFlights')
    fig.update_layout(title_text = "Number of flights per week", 
                        title_x=0.5,
                        title_font_size=18,
                        uniformtext_minsize=8, 
                        uniformtext_mode='hide', 
                        template='none', 
                        paper_bgcolor='#fafafa',
                        plot_bgcolor='#fafafa', 
                        margin=dict(l=50, r=40, t=70, b=70)
                        )
    fig.update_traces(texttemplate='%{text:.2s}', 
                        textposition='outside', 
                        marker_color= 'seaGreen')
    fig.update_yaxes(title_text="Number of flights")
    fig.update_xaxes(title_text="No. of the week")

    return fig

# callback for hour_figure
@app.callback(Output('hour_graph', 'figure'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_hour_figure(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    df_graph = dff.groupby(['WeekNumber','DayOfWeek','Hour']).sum().reset_index()
    df_hour = df_graph.groupby(['Hour']).mean().reset_index().round(decimals=2)
    fig = px.bar(df_hour, x='Hour', y='NumberFlights', text='NumberFlights')
    fig.update_layout(title_text = "Average number of flights per hour of the day", 
                        title_x=0.5,
                        title_font_size=18,
                        uniformtext_minsize=8, 
                        uniformtext_mode='hide', 
                        template='none', 
                        paper_bgcolor='#fafafa',
                        plot_bgcolor='#fafafa', 
                        margin=dict(l=50, r=40, t=70, b=70)
                        )
    fig.update_traces(texttemplate='%{text:.2s}',
                        textposition='outside',
                        marker_color= 'indigo'
                        )
    fig.update_xaxes(dtick=1,title_text="Hour of the day")
    fig.update_yaxes(title_text="Number of flights")

    return fig

# callback for weekday_figure
@app.callback(Output('weekday_graph', 'figure'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_dayofweek_figure(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    df_graph = dff.groupby(['WeekNumber','DayOfWeek']).sum().reset_index()
    test = df_graph.groupby('DayOfWeek').mean().reset_index().round(decimals=2)
    fig = px.pie(test, values='NumberFlights', names='DayOfWeek', title='Average Number of flights per weekday')
    fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=15)
    fig.update_layout(title_text = "Proportion of the french air traffic per day of the week", 
                        title_x=0.5,
                        title_font_size=18,
                        uniformtext_minsize=8, 
                        uniformtext_mode='hide', 
                        template='none', 
                        paper_bgcolor='#fafafa',
                        plot_bgcolor='#fafafa', 
                        margin=dict(l=80, r=80, t=70, b=70),
                        showlegend=False
                        )

    return fig

# callback for data_table
@app.callback(Output('data_table', 'data'),
              [Input('operator_dropdown', 'value'),
              Input('day_dropdown','value'),
              Input('date_picker_range', 'start_date'),
              Input('date_picker_range', 'end_date')])
def make_data_table(operator_selected, dayofweek, start_date,end_date):

    dff = filter_dataframe(df, operator_selected, dayofweek, start_date, end_date)
    df_ope = dff.groupby(['Operator'])[['NumberFlights']].sum().sort_values(by=['NumberFlights'],ascending=False)
    df_model = dff.groupby(['Operator','Model'])[['NumberFlights']].sum().sort_values(by=['NumberFlights'],ascending=False).reset_index()
    df_manuf = dff.groupby(['Operator','Manufacturer'])[['NumberFlights']].sum().sort_values(by=['NumberFlights'],ascending=False).reset_index()
    df_model = df_model.drop_duplicates(subset='Operator').set_index('Operator')
    df_manuf = df_manuf.drop_duplicates(subset='Operator').set_index('Operator')
    df_final = df_ope.join(df_model['Model']).join(df_manuf['Manufacturer']).reset_index()
    df_final.columns = ['Operator','Total No. of flights','Most used aircraft','Favorite manufacturer']
    data = df_final.to_dict('records')

    return data

#Main
#if __name__ == '__main__':
#  app.server.run(debug=True,port = 50004)

if __name__ == '__main__':
    app.server.run(debug=True,port = 50004,host='192.168.1.156') 
