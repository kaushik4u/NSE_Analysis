# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import json

with open('./data/temp/test_data/nifty50.json') as f:
    data = json.load(f)

tickers = []
for i in range(len(data)):
    tickers.append(data[i]['chart']['result'][0]['meta']['symbol'])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def format_data_for_candlestick(ticker_index):
    timedata = timedata= []
    open = high = low = close = volume = []
    for i in range(len(data[ticker_index]['chart']['result'][0]['timestamp'])):    
        timedata.append(datetime.fromtimestamp(data[ticker_index]['chart']['result'][0]['timestamp'][i]))
    open = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['open']
    high = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['high']
    close = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['close']
    low = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['low']
    volume = data[ticker_index]['chart']['result'][0]['indicators']['quote'][0]['volume']
    temp = {'datetime':timedata,'Open':open,'Low':low,'High':high,'Close':close,'Volume':volume}
    df = pd.DataFrame(temp)
    df.set_index('datetime',inplace=True)
    return df

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})
    return dict_list

df = format_data_for_candlestick(35)


###########################################
INCREASING_COLOR = '#17BECF'
DECREASING_COLOR = '#7F7F7F'

INCREASING_COLOR = '#7CFC00'
DECREASING_COLOR = '#FF0000'


data = [ dict(
    type = 'candlestick',
    open = df.Open,
    high = df.High,
    low = df.Low,
    close = df.Close,
    x = df.index,
    yaxis = 'y2',
    name = 'GS',
    increasing = dict( line = dict( color = INCREASING_COLOR ) ),
    decreasing = dict( line = dict( color = DECREASING_COLOR ) ),
) ]

layout=dict()

fig = dict( data=data, layout=layout )
fig['layout'] = dict()
fig['layout']['plot_bgcolor'] = 'rgba(0,0,0,0)'

fig['layout']['xaxis'] = dict( rangeselector = dict( visible = True ) )
fig['layout']['yaxis'] = dict( domain = [0, 0.2], showticklabels = False )
fig['layout']['yaxis2'] = dict( domain = [0.2, 0.8] )
fig['layout']['legend'] = dict( orientation = 'h', y=0.9, x=0.3, yanchor='bottom' )
fig['layout']['margin'] = dict( t=40, b=40, r=40, l=40 )
fig['layout']['height'] = 800
fig['layout']['xaxis'] = dict(type='category', tickmode='auto', nticks=10)

rangeselector=dict(
    visible = True,
    x = 0, y = 0.9,
    bgcolor = 'rgba(150, 200, 250, 0.4)',
    font = dict( size = 13 ),
    buttons=list([
        dict(count=1,
             label='reset',
             step='all'),
        dict(count=1,
             label='6 mo',
             step='month',
             stepmode='backward'),
        dict(count=3,
            label='3 mo',
            step='month',
            stepmode='backward'),
        dict(count=1,
            label='1 mo',
            step='month',
            stepmode='backward'),
        dict(step='all')
    ]))

rangeselector=dict(
    visible = True,
    x = 0, y = 0.9,
    bgcolor = 'rgba(150, 200, 250, 0.4)',
    font = dict( size = 13 ),
    buttons=list([
        dict(count=1,
             label='reset',
             step='all'),
        dict(count=1,
             label='5 day',
             step='day',
             stepmode='backward'),
        dict(count=8,
            label='8 hr',
            step='hour',
            stepmode='backward'),
        dict(count=4,
            label='4 hr',
            step='hour',
            stepmode='backward'),
        dict(step='all')
    ]))
    
fig['layout']['xaxis']['rangeselector'] = rangeselector

def movingaverage(interval, window_size=10):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

mv_y = movingaverage(df.Close)
mv_x = list(df.index)

# Clip the ends
mv_x = mv_x[5:-5]
mv_y = mv_y[5:-5]

fig['data'].append( dict( x=mv_x, y=mv_y, type='scatter', mode='lines', 
                         line = dict( width = 1 ),
                         marker = dict( color = '#E377C2' ),
                         yaxis = 'y2', name='Moving Average' ) )

vwap_y = (df['Volume']*(df['High']+df['Low']+df['Close'])/3).cumsum() / df['Volume'].cumsum()
vwap_x = list(df.index)

df['VWAP'] = vwap_y
df.to_csv('testdata.csv')
fig['data'].append( dict( x=vwap_x, y=vwap_y, type='scatter', mode='lines', 
                         line = dict( width = 1 ),
                         marker = dict( color = '#005BFF' ),
                         yaxis = 'y2', name='VWAP' ) )

colors = []

for i in range(len(df.Close)):
    if i != 0:
        if df.Close[i] > df.Close[i-1]:
            colors.append(INCREASING_COLOR)
        else:
            colors.append(DECREASING_COLOR)
    else:
        colors.append(DECREASING_COLOR)

fig['data'].append( dict( x=df.index, y=df.Volume,                         
                         marker=dict( color=colors ),
                         type='bar', yaxis='y', name='Volume' ) )

print(df)
#################################################################




app.layout = html.Div(children=[
    html.H1(children='Stock Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div(className='div-for-dropdown',
          children=[
              dcc.Dropdown(id='stockselector',
                           #options=get_options(df['stock'].unique()),
                           options=get_options(tickers),
                           multi=False,
                           #value=[df['stock'].sort_values()[0]],
                           value=[tickers[0]],
                           style={'backgroundColor': '#1E1E1E'},
                           className='stockselector')
                    ],
          style={'color': '#1E1E1E'}),

    dcc.Graph(
        id='candlestick-graph',
        # figure={
        #     'data': [
        #         {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        #         {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        #     ],
        #     'layout': {
        #         'title': 'Dash Data Visualization'
        #     }
        # }
        # figure = go.Figure(data=[go.Candlestick(x=df['datetime'],
        #         open=df['Open'],
        #         high=df['High'],
        #         low=df['Low'],
        #         close=df['Close'])],
        #         layout=go.Layout(
        #             height=800,             
                    
                    
        #         )),
        figure = fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)