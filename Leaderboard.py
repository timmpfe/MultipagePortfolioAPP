import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
from flask import Flask

pd.options.mode.chained_assignment = None  # default='warn'


def get_data():
    data = pd.read_csv('leaderboard.txt', header=None)
    data.columns = ['Nummer', 'Sharpe Ratio', 'Sharpe Ratio 2', 'Endwert', 'Absoluter Ertrag 2',
                    'Ertrag in % p.a.', '% Ertrag 2']

    for i in range(len(data)):
        data.loc[i, 'Nummer'] = data.loc[i, 'Nummer'].replace(data.loc[i, 'Nummer'], data.loc[i, 'Nummer'][1:])
        data.loc[i, '% Ertrag 2'] = data.loc[i, '% Ertrag 2'].replace(data.loc[i, '% Ertrag 2'],
                                                                      data.loc[i, '% Ertrag 2'][:-1])
    data = data.astype(float).round(4)

    data2 = data.drop_duplicates(subset=['Nummer'])
    num1 = int(data2.Nummer.iloc[-1])
    data1a = data2[['Nummer', 'Sharpe Ratio', 'Endwert', 'Ertrag in % p.a.']]
    data1a.loc[data1a['Nummer'] == 0, 'Nummer'] = 'Buffett'
    data1b = data2[['Nummer', 'Sharpe Ratio 2', 'Absoluter Ertrag 2', '% Ertrag 2']]
    data1b.columns = ['Nummer', 'Sharpe Ratio', 'Endwert', 'Ertrag in % p.a.']
    data1b.loc[data1b['Nummer'] == 0, 'Nummer'] = 'Dow Jones'
    data1 = data1a.append(data1b)
    data1 = data1.sort_values(by=['Sharpe Ratio'], ascending=False)
    data1['Rang'] = range(len(data1))
    data1['Rang'] += 1
    Platz = data1.loc[data1['Nummer'] == num1, 'Rang'].iloc[0]
    data1 = data1[['Rang', 'Nummer', 'Endwert', 'Sharpe Ratio', 'Ertrag in % p.a.']]
    return data1, num1, Platz


init_data, init_num, init_platz = get_data()

style_text = {'textAlign': 'center', 'color': '#003361'}

server = Flask(__name__, static_url_path="", static_folder="static")

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                suppress_callback_exceptions=True)

app.layout = html.Div([
    dbc.Container([
        dbc.Row(html.Img(src='https://vtlogo.com/wp-content/uploads/2020/05/universitaet-innsbruck-vector-logo.png',
                         style={'height': '15%', 'width': '15%'})),
        dbc.Row(html.H1('"A random walk down Wallstreet"', style=style_text)),
        html.Br(),
        dbc.Row(html.H3('Leaderboard', style=style_text)),
        html.Br(),
        dbc.Row([
            dbc.Col(html.H6('Sie sind auf Platz: {}'.format(init_platz), id="platz-text",
                            style={'textAlign': 'center', 'color': '#f39200'})),
            dbc.Col(html.H6('Ihre Nummmer lautet: {}'.format(int(init_num)), id="nummer-text",
                            style={'textAlign': 'center', 'color': '#f39200'}))]),
        html.Br(),
        dbc.Row(dash_table.DataTable(init_data.to_dict('records'), id="leaderboard",
                                     columns=[{"name": i, "id": i} for i in init_data.columns],
                                     style_data_conditional=[
                                         {
                                             'if': {
                                                 'filter_query': '{Nummer} = "Buffett"',
                                             },
                                             'backgroundColor': '#003361',
                                             'color': '#f39200'
                                         },
{
                                             'if': {
                                                 'filter_query': '{Nummer} = "Dow Jones"',
                                             },
                                             'backgroundColor': '#f39200',
                                             'color': '#003361'
                                         }
                                     ])
                ),
        # Der Timer triggered die "updateTable" Funktion alle 5 Sekunden
        dash.dcc.Interval(id="timer", interval=5000)
    ])
])


@app.callback([Output("leaderboard", "data"), Output("platz-text", "children"), Output("nummer-text", "children")],
              [Input("timer", "n_intervals")])
def updateTable(n_intervals):
    # Die Funktion liest dann die Daten ein ...
    data, num, platz = get_data()
    # ... und gibt sie an Dash zurück. Dank der Annotation weiß Dash, wo die Daten dann hingehören
    return get_data()[0].to_dict('records'), 'Sie sind auf Platz: {}'.format(platz), 'Ihre Nummmer lautet: {}'.format(
        num)


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8000)

