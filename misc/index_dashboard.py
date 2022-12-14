import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, timedelta
import requests
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5],
                    'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

proxyDict = {

}
def fetch_indices():
    indices_list = ['DJI', 'IXIC', 'GSPC', 'N225', 'HSI', 'NSEI']
    for index in indices_list:
        fetch_live_feed(index)


def fetch_live_feed(index):
    # print(int(datetime.now().timestamp()))
    prevDay = datetime.now() + timedelta(days=-5)
    # print(int(prevDay.timestamp()))
    yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/^' + index + '?symbol=^' + index + \
        '&period1=' + str(int(prevDay.timestamp())) + '&period2=' + \
        str(int(datetime.now().timestamp())) + '&interval=1m'
    print(yahoo_url)
    res = requests.get(yahoo_url, proxies = proxyDict)
    # print(res.text)
    fileName = index + '.json'
    with open('./data/temp/indices/'+fileName, 'w', encoding='utf-8') as outfile:
        json.dump(json.JSONDecoder().decode(res.text), outfile)
    print('Data fetched : ', datetime.now().strftime('%d-%m-%Y %HH:%MM'))


if __name__ == '__main__':
    fetch_indices()
    app.run_server(debug=True)
