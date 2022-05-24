import dash
from dash import Dash, dcc, html, Input, Output, State, callback

import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate

import pandas as pd

# just that the warning that a copy on an existing df is made does not pop up
pd.options.mode.chained_assignment = None

from flask import Flask

server = Flask(__name__, static_url_path="", static_folder="static")

'''Create an Dash-Environment on the server'''

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP],
                # meta_tags is used that the page adjusts to the screen size
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
# the index page is important that the links between the pages work
index_page = html.Div([
    dcc.Link('Random', href='/page-1'),
    html.Br(),
    dcc.Link('Historische Information', href='/page-2'),
    html.Br(),
    dcc.Link('Summary', href='/page-3'),
])

'''-------------------------------------------Page 1--------------------------------------------'''
style_button_1 = {'display': 'inline-block', 'min-width': '250px', 'min-height': '170px',
                  'margin-top': '5px', 'margin-left': '5px', 'background-color': '#f39200', 'color': '#003361'}

style_text = {'textAlign': 'center', 'color': '#003361'}

page_1_layout = html.Div([
    # The memory store reverts to the default on every page refresh
    dcc.Store(id='user_portfolio_1'),
    dcc.Store(id='graph_data_1'),
    dcc.Store(id='level_1'),

    dbc.Container([
        dbc.Row(html.Img(src='https://vtlogo.com/wp-content/uploads/2020/05/universitaet-innsbruck-vector-logo.png',
                         style={'height': '15%', 'width': '15%'})),
        dbc.Row(html.H1('"A random walk down Wallstreet"', style=style_text)),
        dbc.Row(html.H3(id='clicks_1', style=style_text)),
        dbc.Row([dbc.Col(html.H6('Sie befinden sich in Periode', style={'textAlign': 'left', 'color': '#003361'})),
                 dbc.Col(dcc.Link('Weiter', href='/page-2'), align='end')], justify="between"),
        dbc.Row(dcc.Slider(id="slider_1", min=0, max=2, step=1)),

        # Seperated into 5 rows à 6 stocks - a total of 30 stocks can be selected
        dbc.Row([
            dbc.Col(dbc.Button('Aktie 01', id='memory-button_1', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 02', id='memory-button_2', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 03', id='memory-button_3', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 04', id='memory-button_4', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 05', id='memory-button_5', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 06', id='memory-button_6', style=style_button_1, outline=True))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button('Aktie 07', id='memory-button_7', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 08', id='memory-button_8', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 09', id='memory-button_9', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 10', id='memory-button_10', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 11', id='memory-button_11', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 12', id='memory-button_12', style=style_button_1, outline=True))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button('Aktie 13', id='memory-button_13', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 14', id='memory-button_14', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 15', id='memory-button_15', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 16', id='memory-button_16', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 17', id='memory-button_17', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 18', id='memory-button_18', style=style_button_1, outline=True))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button('Aktie 19', id='memory-button_19', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 20', id='memory-button_20', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 21', id='memory-button_21', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 22', id='memory-button_22', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 23', id='memory-button_23', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 24', id='memory-button_24', style=style_button_1, outline=True))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button('Aktie 25', id='memory-button_25', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 26', id='memory-button_26', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 27', id='memory-button_27', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 28', id='memory-button_28', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 29', id='memory-button_29', style=style_button_1, outline=True)),
            dbc.Col(dbc.Button('Aktie 30', id='memory-button_30', style=style_button_1, outline=True))]
        ),
    ], fluid=True),
])


# ------------------------------------- CALLBACKS PAGE 1 -----------------------------------------
@app.callback(Output(component_id='user_portfolio_1', component_property='data'),
              [Input(component_id='memory-button_{}'.format(stock_id_1), component_property='n_clicks')
               for stock_id_1 in range(1, 31)])
def on_click_1(*n_clicks, **kwargs_1):
    # Replace Nones by zeros
    n_clicks = tuple(0 if n_click_1 is None else n_click_1 for n_click_1 in n_clicks)
    return n_clicks


@app.callback(Output(component_id='clicks_1', component_property='children'),
              [Input(component_id='memory-button_{}'.format(stock_id_1), component_property='n_clicks')
               for stock_id_1 in range(1, 31)])
def displayclick_1(*n_clicks):
    n_clicks = tuple(0 if n_click_1 is None else n_click_1 for n_click_1 in n_clicks)
    clicks_1 = sum(n_clicks)
    if clicks_1 < 10:
        free_clicks_1 = 10 - clicks_1
        msg_1 = 'Wählen Sie bitte {} Aktien aus'.format(free_clicks_1)
    elif clicks_1 >= 10 and clicks_1 < 20:
        free_clicks_1 = 20 - clicks_1
        msg_1 = 'Wählen Sie bitte {} Aktien aus'.format(free_clicks_1)
    else:
        msg_1 = 'Bitte klicken Sie auf weiter'
    return html.Div(msg_1)


@app.callback([Output(component_id='graph_data_1', component_property='data'),
               Output(component_id='slider_1', component_property='value')],
              Input(component_id='user_portfolio_1', component_property='data'),
              State('graph_data_1', 'data'))
def on_portfolio_change_1(portfolio_1, graph_data_1):
    if graph_data_1 is None:
        if sum(portfolio_1) == 10:
            return portfolio_1, 1
        else:
            return graph_data_1, 0
    else:
        if sum(portfolio_1) == 20:
            portfolio_21 = [a - b for a, b in zip(portfolio_1, graph_data_1)]
            with open('weights_random.txt', 'a') as f:
                f.write(str((graph_data_1, portfolio_21)) + "\n")
            return (portfolio_1, portfolio_21), 2
        else:
            return graph_data_1, 1


'''-------------------------------------------------PAGE 2-----------------------------------------------------'''

style_button = {'display': 'inline-block', 'width': '250px', 'height': '200px',
                'margin-top': '2px', 'margin-left': '2px'}

page_2_layout = html.Div([
    # The memory store reverts to the default on every page refresh
    dcc.Store(id='user_portfolio'),
    dcc.Store(id='graph_data'),
    dcc.Store(id='level'),

    dbc.Container([
        dbc.Row(html.Img(src='https://vtlogo.com/wp-content/uploads/2020/05/universitaet-innsbruck-vector-logo.png',
                         style={'height': '15%', 'width': '15%'})),
        dbc.Row(html.H1('"A random walk down Wallstreet"', style=style_text)),

        dbc.Row(html.H3(id='clicks', style=style_text)),

        dbc.Row([dbc.Col(html.H6('Sie befinden sich in Periode', style={'textAlign': 'left', 'color': '#003361'})),
                 dbc.Col(dcc.Link('Weiter', href='/page-3'), align='end')], justify="between"),
        dbc.Row(dcc.Slider(id="slider", min=0, max=2, step=1)),

        # Seperated into 5 rows à 6 stocks - a total of 30 stocks can be selected
        dbc.Row([
            dbc.Col(dbc.Button(id='button_1',
                               children=[dbc.CardImg(id="button_image_1", src='/AAPL_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_2',
                               children=[dbc.CardImg(id="button_image_2", src='AMGN_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_3',
                               children=[dbc.CardImg(id="button_image_3", src='/AXP_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_4',
                               children=[dbc.CardImg(id="button_image_4", src='/BA_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_5',
                               children=[dbc.CardImg(id="button_image_5", src='/CAT_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_6',
                               children=[dbc.CardImg(id="button_image_6", src='/CRM_2007_2012.png')],
                               outline=True, style=style_button))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button(id='button_7',
                               children=[dbc.CardImg(id="button_image_7", src='/CSCO_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_8',
                               children=[dbc.CardImg(id="button_image_8", src='/CVX_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_9',
                               children=[dbc.CardImg(id="button_image_9", src='/DIS_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_10',
                               children=[dbc.CardImg(id="button_image_10", src='/GE_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_11',
                               children=[dbc.CardImg(id="button_image_11", src='/GS_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_12',
                               children=[dbc.CardImg(id="button_image_12", src='/HD_2007_2012.png')],
                               outline=True, style=style_button))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button(id='button_13',
                               children=[dbc.CardImg(id="button_image_13", src='/HON_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_14',
                               children=[dbc.CardImg(id="button_image_14", src='/IBM_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_15',
                               children=[dbc.CardImg(id="button_image_15", src='/INTC_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_16',
                               children=[dbc.CardImg(id="button_image_16", src='/JNJ_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_17',
                               children=[dbc.CardImg(id="button_image_17", src='/JPM_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_18',
                               children=[dbc.CardImg(id="button_image_18", src='/KO_2007_2012.png')],
                               outline=True, style=style_button))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button(id='button_19',
                               children=[dbc.CardImg(id="button_image_19", src='/MCD_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_20',
                               children=[dbc.CardImg(id="button_image_20", src='/MMM_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_21',
                               children=[dbc.CardImg(id="button_image_21", src='/MRK_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_22',
                               children=[dbc.CardImg(id="button_image_22", src='/MSFT_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_23',
                               children=[dbc.CardImg(id="button_image_23", src='/NKE_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_24',
                               children=[dbc.CardImg(id="button_image_24", src='/PG_2007_2012.png')],
                               outline=True, style=style_button))]
        ),
        dbc.Row([
            dbc.Col(dbc.Button(id='button_25',
                               children=[dbc.CardImg(id="button_image_25", src='/TRV_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_26',
                               children=[dbc.CardImg(id="button_image_26", src='/UNH_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_27',
                               children=[dbc.CardImg(id="button_image_27", src='/V_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_28',
                               children=[dbc.CardImg(id="button_image_28", src='/VZ_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_29',
                               children=[dbc.CardImg(id="button_image_29", src='/WBA_2007_2012.png')],
                               outline=True, style=style_button)),
            dbc.Col(dbc.Button(id='button_30',
                               children=[dbc.CardImg(id="button_image_30", src='/WMT_2007_2012.png')],
                               outline=True, style=style_button))]
        ),
    ], fluid=True),
])


@app.callback(Output(component_id='user_portfolio', component_property='data'),
              [Input(component_id='button_{}'.format(stock_id), component_property='n_clicks') for stock_id in
               range(1, 31)])
def on_click(*n_clicks, **kwargs):
    # Replace Nones by zeros
    n_clicks = tuple(0 if n_click is None else n_click for n_click in n_clicks)
    return n_clicks


@app.callback([Output(component_id='clicks', component_property='children')] +
              [Output(component_id='button_image_{}'.format(stock_id), component_property='src') for stock_id in
               range(1, 31)],
              [Input(component_id='button_{}'.format(stock_id), component_property='n_clicks') for stock_id in
               range(1, 31)])
def displayClick(*n_clicks):
    n_clicks = tuple(0 if n_click is None else n_click for n_click in n_clicks)
    clicks = sum(n_clicks)
    # This is the path for the pictures, which should be displayed in the different periods
    image_sources1 = ['/AAPL_2007_2012.png', 'AMGN_2007_2012.png', '/AXP_2007_2012.png', '/BA_2007_2012.png',
                      '/CAT_2007_2012.png', '/CRM_2007_2012.png', '/CSCO_2007_2012.png', '/CVX_2007_2012.png',
                      '/DIS_2007_2012.png', '/GE_2007_2012.png', '/GS_2007_2012.png', '/HD_2007_2012.png',
                      '/HON_2007_2012.png', '/IBM_2007_2012.png', '/INTC_2007_2012.png', '/JNJ_2007_2012.png',
                      '/JPM_2007_2012.png', '/KO_2007_2012.png', '/MCD_2007_2012.png', '/MMM_2007_2012.png',
                      '/MRK_2007_2012.png', '/MSFT_2007_2012.png', '/NKE_2007_2012.png', '/PG_2007_2012.png',
                      '/TRV_2007_2012.png', '/UNH_2007_2012.png', '/V_2007_2012.png', '/VZ_2007_2012.png',
                      '/WBA_2007_2012.png', '/WMT_2007_2012.png']
    image_sources2 = ['/AAPL_2012_2017.png', 'AMGN_2012_2017.png', '/AXP_2012_2017.png', '/BA_2012_2017.png',
                      '/CAT_2012_2017.png', '/CRM_2012_2017.png', '/CSCO_2012_2017.png', '/CVX_2012_2017.png',
                      '/DIS_2012_2017.png', '/GE_2012_2017.png', '/GS_2012_2017.png', '/HD_2012_2017.png',
                      '/HON_2012_2017.png', '/IBM_2012_2017.png', '/INTC_2012_2017.png', '/JNJ_2012_2017.png',
                      '/JPM_2012_2017.png', '/KO_2012_2017.png', '/MCD_2012_2017.png', '/MMM_2012_2017.png',
                      '/MRK_2012_2017.png', '/MSFT_2012_2017.png', '/NKE_2012_2017.png', '/PG_2012_2017.png',
                      '/TRV_2012_2017.png', '/UNH_2012_2017.png', '/V_2012_2017.png', '/VZ_2012_2017.png',
                      '/WBA_2012_2017.png', '/WMT_2012_2017.png']

    # depending on the Clicks, the list of pictures changes
    if clicks < 10:
        free_clicks = 10 - clicks
        msg = 'Wählen Sie bitte {} Aktien aus'.format(free_clicks)
        image_sources = image_sources1
    elif clicks >= 10 and clicks < 20:
        free_clicks = 20 - clicks
        msg = 'Wählen Sie bitte {} Aktien aus'.format(free_clicks)
        # At this point, we change the values of the image locations
        image_sources = image_sources2
    else:
        msg = 'Bitte klicken Sie auf weiter'
        image_sources = image_sources2

    # The "*" symbol tells Dash to unpack the list, meaning instead of returning the list it will return the elements
    # of the list
    return html.Div(msg), *image_sources


@app.callback([Output(component_id='graph_data', component_property='data'),
               Output(component_id='slider', component_property='value')],
              Input(component_id='user_portfolio', component_property='data'),
              State('graph_data', 'data'))
def on_portfolio_change(portfolio, graph_data):
    if graph_data is None:
        if sum(portfolio) == 10:
            return portfolio, 1
        else:
            return graph_data, 0
    else:
        if sum(portfolio) == 20:
            portfolio_2 = [a - b for a, b in zip(portfolio, graph_data)]
            with open('weights_historical.txt', 'a') as f:
                f.write(str((graph_data, portfolio_2)) + "\n")
            return (portfolio, portfolio_2), 2
        else:
            return graph_data, 1


'''--------------------------------------------Summary Page --------------------------------------------------------'''

'''Create the App Layout'''
page_3_layout = html.Div([
    dbc.Container([
        dcc.Interval(id='my_interval', interval=1000, n_intervals=0),
        dbc.Row(html.Img(src='https://vtlogo.com/wp-content/uploads/2020/05/universitaet-innsbruck-vector-logo.png',
                         style={'height': '15%', 'width': '15%'})),
        dbc.Row(html.H1('"A random walk down Wallstreet"', style=style_text)),

        dbc.Row(html.H3('Zusammenfassung Ihres Portfolios', style=style_text)),
        dbc.Row(dcc.Link('Starte Neu', href='/page-1')),
        dbc.Row(dbc.Table(

            children=[],
            id="table",
            color="primary",
        )),
        dbc.Row(dcc.Graph(id='my_Graph', figure={})),
        dbc.Row([
            dbc.Col(dcc.Graph(id='my_random_pie', figure={}), width=6),
            dbc.Col(dcc.Graph(id='my_historical_pie', figure={}), width=6)
        ]),
    ])
])

@app.callback(
    [Output('my_Graph', 'figure'),
     Output('my_random_pie', 'figure'),
     Output('my_historical_pie', 'figure'),
     Output('table', 'children')],
    [Input('my_interval', 'n_intervals')]
)
def update_summary(num):
    if num == 0:
        raise PreventUpdate
    else:
        # the only purpose of y_data is that it runs the whole code in the else function
        y_data = num

        benchmark = pd.read_csv('benchmark1.csv', parse_dates=['Date'])
        benchmark.index = pd.to_datetime(benchmark['Date'])
        dff = pd.read_csv('stocks.csv')
        dff = dff[['Date', 'Symbols', 'Close']]
        dff = pd.pivot_table(dff, values=['Close'], index=['Date'], columns=['Symbols'])
        dff = dff.pct_change()
        dff = dff.droplevel(level=0, axis=1)
        dff += 1

        fr = pd.read_csv('weights_random.txt', header=None)
        fh = pd.read_csv('weights_historical.txt', header=None)

        df = dff.loc['2012-01-04':'2017-01-01']
        df2 = dff.loc['2017-01-01':]

        fr.columns = ['AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'GE', 'GS', 'HD', 'HON', 'IBM',
                      'INTC',
                      'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA',
                      'WMT',
                      'AAPL_1', 'AMGN_1', 'AXP_1', 'BA_1', 'CAT_1', 'CRM_1', 'CSCO_1', 'CVX_1', 'DIS_1', 'GE_1', 'GS_1',
                      'HD_1', 'HON_1', 'IBM_1', 'INTC_1', 'JNJ_1', 'JPM_1', 'KO_1', 'MCD_1', 'MMM_1', 'MRK_1', 'MSFT_1',
                      'NKE_1', 'PG_1', 'TRV_1', 'UNH_1', 'V_1', 'VZ_1', 'WBA_1', 'WMT_1']
        for i in range(len(fr)):
            fr.loc[i, 'WMT'] = fr.loc[i, 'WMT'].replace(fr.loc[i, 'WMT'], fr.loc[i, 'WMT'][:-1])
            fr.loc[i, 'AAPL'] = fr.loc[i, 'AAPL'].replace(fr.loc[i, 'AAPL'], fr.loc[i, 'AAPL'][2:])
            fr.loc[i, 'AAPL_1'] = fr.loc[i, 'AAPL_1'].replace(fr.loc[i, 'AAPL_1'], fr.loc[i, 'AAPL_1'][2:])
            fr.loc[i, 'WMT_1'] = fr.loc[i, 'WMT_1'].replace(fr.loc[i, 'WMT_1'], fr.loc[i, 'WMT_1'][:-2])

        fr = fr.astype(int)

        fh.columns = ['AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'GE', 'GS', 'HD', 'HON', 'IBM',
                      'INTC',
                      'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA',
                      'WMT',
                      'AAPL_1', 'AMGN_1', 'AXP_1', 'BA_1', 'CAT_1', 'CRM_1', 'CSCO_1', 'CVX_1', 'DIS_1', 'GE_1', 'GS_1',
                      'HD_1', 'HON_1', 'IBM_1', 'INTC_1', 'JNJ_1', 'JPM_1', 'KO_1', 'MCD_1', 'MMM_1', 'MRK_1', 'MSFT_1',
                      'NKE_1', 'PG_1', 'TRV_1', 'UNH_1', 'V_1', 'VZ_1', 'WBA_1', 'WMT_1']
        for i in range(len(fh)):
            fh.loc[i, 'WMT'] = fh.loc[i, 'WMT'].replace(fh.loc[i, 'WMT'], fh.loc[i, 'WMT'][:-1])
            fh.loc[i, 'AAPL'] = fh.loc[i, 'AAPL'].replace(fh.loc[i, 'AAPL'], fh.loc[i, 'AAPL'][2:])
            fh.loc[i, 'AAPL_1'] = fh.loc[i, 'AAPL_1'].replace(fh.loc[i, 'AAPL_1'], fh.loc[i, 'AAPL_1'][2:])
            fh.loc[i, 'WMT_1'] = fh.loc[i, 'WMT_1'].replace(fh.loc[i, 'WMT_1'], fh.loc[i, 'WMT_1'][:-2])

        fh = fh.astype(int)

        period_1_r = fr[
            ['AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'GE', 'GS', 'HD', 'HON', 'IBM', 'INTC',
             'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT', ]]
        period_2_r = fr[
            ['AAPL_1', 'AMGN_1', 'AXP_1', 'BA_1', 'CAT_1', 'CRM_1', 'CSCO_1', 'CVX_1', 'DIS_1', 'GE_1', 'GS_1',
             'HD_1', 'HON_1', 'IBM_1', 'INTC_1', 'JNJ_1', 'JPM_1', 'KO_1', 'MCD_1', 'MMM_1', 'MRK_1', 'MSFT_1',
             'NKE_1', 'PG_1', 'TRV_1', 'UNH_1', 'V_1', 'VZ_1', 'WBA_1', 'WMT_1']]

        period_1_h = fh[
            ['AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'GE', 'GS', 'HD', 'HON', 'IBM', 'INTC',
             'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT', ]]
        period_2_h = fh[
            ['AAPL_1', 'AMGN_1', 'AXP_1', 'BA_1', 'CAT_1', 'CRM_1', 'CSCO_1', 'CVX_1', 'DIS_1', 'GE_1', 'GS_1',
             'HD_1', 'HON_1', 'IBM_1', 'INTC_1', 'JNJ_1', 'JPM_1', 'KO_1', 'MCD_1', 'MMM_1', 'MRK_1', 'MSFT_1',
             'NKE_1', 'PG_1', 'TRV_1', 'UNH_1', 'V_1', 'VZ_1', 'WBA_1', 'WMT_1']]

        symbols = ['AAPL_1', 'AMGN_1', 'AXP_1', 'BA_1', 'CAT_1', 'CRM_1', 'CSCO_1', 'CVX_1', 'DIS_1', 'GE_1', 'GS_1',
                   'HD_1', 'HON_1', 'IBM_1', 'INTC_1', 'JNJ_1', 'JPM_1', 'KO_1', 'MCD_1', 'MMM_1', 'MRK_1', 'MSFT_1',
                   'NKE_1', 'PG_1', 'TRV_1', 'UNH_1', 'V_1', 'VZ_1', 'WBA_1', 'WMT_1']

        df2.columns = symbols

        '''-------------------------------Pie Charts for Portfolio allocation----------------------------------------'''

        help_list = ['Apple', 'Amgen', 'American Express', 'Boeing', 'Caterpillar',
                     'Salesforce', 'Cisco Systems', 'Chevron', 'Disney',
                     'General Electric', 'Goldman Sachs', 'Home Depot', 'Honeywell', 'IBM',
                     'Intel', 'Johnson & Johnson', 'JPMorgan Chase ', 'Coca-Cola',
                     'McDonald’s', '3M', 'Merck', 'Microsoft',
                     'Nike', 'Procter & Gamble', 'Travelers Companies', 'UnitedHealth',
                     'Visa', 'Verizon', 'Walgreens Boots Alliance', 'Walmart']

        pf_rand = fr[['AAPL_1', 'AMGN_1', 'AXP_1', 'BA_1', 'CAT_1', 'CRM_1', 'CSCO_1', 'CVX_1', 'DIS_1', 'GE_1', 'GS_1',
                      'HD_1', 'HON_1', 'IBM_1', 'INTC_1', 'JNJ_1', 'JPM_1', 'KO_1', 'MCD_1', 'MMM_1', 'MRK_1', 'MSFT_1',
                      'NKE_1', 'PG_1', 'TRV_1', 'UNH_1', 'V_1', 'VZ_1', 'WBA_1', 'WMT_1']].iloc[-1:]

        pf_hist = fh[['AAPL_1', 'AMGN_1', 'AXP_1', 'BA_1', 'CAT_1', 'CRM_1', 'CSCO_1', 'CVX_1', 'DIS_1', 'GE_1', 'GS_1',
                      'HD_1',
                      'HON_1', 'IBM_1', 'INTC_1', 'JNJ_1', 'JPM_1', 'KO_1', 'MCD_1', 'MMM_1', 'MRK_1', 'MSFT_1',
                      'NKE_1', 'PG_1', 'TRV_1', 'UNH_1', 'V_1', 'VZ_1', 'WBA_1', 'WMT_1']].iloc[-1:]

        help_dict = {'Stock': help_list, 'Amount': pf_rand.iloc[0]}
        stock_diver_ran = pd.DataFrame(help_dict)
        stock_diver_ran = stock_diver_ran.loc[~(stock_diver_ran['Amount'] == 0)]

        help_dict2 = {'Stock': help_list, 'Amount': pf_hist.iloc[0]}
        stock_diver_hist = pd.DataFrame(help_dict2)
        stock_diver_hist = stock_diver_hist.loc[~(stock_diver_hist['Amount'] == 0)]

        pie_random = px.pie(stock_diver_ran, values='Amount', names='Stock', title='Basierend auf keinen Informationen')
        pie_historical = px.pie(stock_diver_hist, values='Amount', names='Stock',
                                title='Basierend auf historischen Informationen')

        '''-------------------------------Portfolio Values-----------------------------------------------'''
        # period 1 random
        period_1_r *= 10000
        index = period_1_r.index[-1]
        period_1_r.rename(index={index: '2012-01-03'}, inplace=True)
        period_1_r = pd.DataFrame(period_1_r.loc['2012-01-03']).T
        period_r1 = df.append(period_1_r).sort_index().cumprod()

        # period 2 random
        period_2_r *= period_r1.iloc[-1].sum() / 10
        index = period_2_r.index[-1]
        period_2_r.rename(index={index: '2017-01-01'}, inplace=True)
        period_2_r = pd.DataFrame(period_2_r.loc['2017-01-01']).T
        period_r2 = df2.append(period_2_r).sort_index().cumprod()
        period_r2.iloc[-1].sum()

        # period 1 historical
        period_1_h *= 10000
        index = period_1_h.index[-1]
        period_1_h.rename(index={index: '2012-01-03'}, inplace=True)
        period_1_h = pd.DataFrame(period_1_h.loc['2012-01-03']).T
        period_h1 = df.append(period_1_h).sort_index().cumprod()

        # period 2 historical
        period_2_h *= period_h1.iloc[-1].sum() / 10
        index = period_2_h.index[-1]
        period_2_h.rename(index={index: '2017-01-01'}, inplace=True)
        period_2_h = pd.DataFrame(period_2_h.loc['2017-01-01']).T
        period_h2 = df2.append(period_2_h).sort_index().cumprod()

        portfolio_values_p1 = pd.concat([period_r1.sum(axis=1), period_h1.sum(axis=1)], axis=1)
        portfolio_values_p2 = pd.concat([period_r2.sum(axis=1), period_h2.sum(axis=1)], axis=1)

        portfolio_values = pd.concat([portfolio_values_p1, portfolio_values_p2], axis=0)
        portfolio_values.columns = ['Random', 'Historisch']

        portfolio_values.index = pd.to_datetime(portfolio_values.index)
        Graph = pd.concat([portfolio_values, benchmark], axis=1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Graph['Date'], y=Graph['Dow Jones'],
                                 mode='lines', name='Dow Jones Index', line_color='#000000'))
        fig.add_trace(go.Scatter(x=Graph['Date'], y=Graph['Buffett'],
                                 mode='lines', name='Buffett', line_color='#0080ff'))
        fig.add_trace(go.Scatter(x=Graph['Date'], y=Graph['Random'],
                                 mode='lines', name='Random', line_color='#ff9999'))
        fig.add_trace(go.Scatter(x=Graph['Date'], y=Graph['Historisch'],
                                 mode='lines', name='Historisch', line_color='#ff6666'))

        '''------------------------------------Calculating Sharpe Ratio------------------------------------------------------'''

        pct_change_h = Graph['Historisch'].pct_change()
        mean_h = pct_change_h.sum() / len(pct_change_h)
        dev_h = [(x - mean_h) ** 2 for x in pct_change_h]
        dev_h[0] = 0
        var_h = sum(dev_h) / (len(pct_change_h - 1))
        stdev_h = var_h ** (1 / 2)
        sr_h = (mean_h * 252) / (stdev_h * 252 ** (1 / 2))

        pct_change_r = Graph['Random'].pct_change()
        mean_r = pct_change_r.sum() / len(pct_change_r)
        dev_r = [(x - mean_r) ** 2 for x in pct_change_r]
        dev_r[0] = 0
        var_r = sum(dev_r) / (len(pct_change_r - 1))
        stdev_r = var_r ** (1 / 2)
        sr_r = (mean_r / stdev_r) * 252 ** (1 / 2)

        Abs_Ret_R = round(Graph.iloc[-1]['Random'], 2)
        Abs_Ret_H = round(Graph.iloc[-1]['Historisch'], 2)

        Tot_Ret_R = round(((Graph.iloc[-1]['Random'] / Graph.iloc[0]['Random']) ** (1 / 10) - 1) * 100, 2)
        Tot_Ret_H = round(((Graph.iloc[-1]['Historisch'] / Graph.iloc[0]['Historisch']) ** (1 / 10) - 1) * 100, 2)

        number_player = len(fr)

        with open('leaderboard.txt', 'a') as f:
            f.write(str((number_player, sr_r, sr_h, Abs_Ret_R, Abs_Ret_H, Tot_Ret_R, Tot_Ret_H)) + "\n")

        table_header = [html.Thead(html.Tr([html.Th("Portfolio"), html.Th("Endwert"),
                                            html.Th("Absoluter Ertrag in % p.a."), html.Th("Sharpe Ratio")]))]

        row_1 = html.Tr([html.Td("Random"), html.Td(Abs_Ret_R),
                         html.Td(Tot_Ret_R), html.Td(round(sr_r, 2))])

        row_2 = html.Tr([html.Td("Historische Information"), html.Td(Abs_Ret_H),
                         html.Td(Tot_Ret_H), html.Td(round(sr_h, 2))])

        table_body = [html.Tbody([row_1, row_2])]

        table = table_header + table_body

        return fig, pie_random, pie_historical, table


# Update the index
@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page when the user uses a wrong url


if __name__ == '__main__':
    app.run_server(debug=True)

