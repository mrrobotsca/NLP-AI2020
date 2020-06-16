
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table_experiments as dt
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from plotly import tools
import dash_table
import pandas as pd
import dash_daq as daq
import numpy
import datetime
import os
import time
import copy
import sys
import flask
from datetime import datetime
import base64
import datetime
import io
import json
import urllib

global df

#################################################################
# app = dash.Dash(name='app', sharing=True, server=server,
#                 url_base_pathname='/mtce/')
# new = pd.read_csv(r'D:\web\dash\mtce\tot.csv', sep=";", error_bad_lines=False, low_memory=False)

LOGFILE = 'examples/run_log.csv'
app = dash.Dash(__name__)
server = app.server
new = pd.read_csv('tot.csv', sep=";", error_bad_lines=False, low_memory=False)

dir_name = r"C:\Users\dk0086\Documents\instantclient_12_2"

map = pd.DataFrame()
new['date'] = pd.to_datetime(new['date'])
new.sort_values(by=['date'])
map = new.copy()

mapbox_access_token = 'pk.eyJ1IjoiZGswMDg2IiwiYSI6ImNqcnYyanRzYTMxbzI0M2w5aTM4dXJlZHMifQ.G7PbV1tCtLq2lDo3_-yJmw'


division = new.DIV.unique()
division.sort()
technicien = new.Technicien.unique()
technicien.sort()
territoires = new.Territoires.unique()
territoires.sort()
namess = {'Territoire': territoires,
          'Division': division, 'Technicien': technicien}

TYP = new.TYPE_CODE.unique()
TYP.sort()




theme = {
    'dark': False,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E'
}

layout = dict(
    autosize=True,
    height=800,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Cumulatif',
)
layoutt = dict(
    autosize=True,
    height=800,
    barmode='stack',
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Cumulatif - Nb lancés (en haut) et confirmés (en bas)',
)


layout_map = dict(
    autosize=True,
    height=1000,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    # margin=dict(
    #     l=15,
    #     r=35,
    #     b=35,
    #     t=45

    # ),
    xaxis=[],
    yaxis=[],
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Visuel Sur Une Carte',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="mapbox://styles/mapbox/light-v9",
        center=dict(
            lon=-73.8703,
            lat=45.5581
        ),
        zoom=6,
        pitch=30,
    )
)



def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])]

 # Body
        + [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def div_graph(name):
    """Generates an html Div containing graph and control options for smoothing and display, given the name"""
    return html.Div(
        [
            html.Details([
                html.Summary("Nombre d'avis par territoire"),

                html.Div(
                         [
                             # html.P("Leads count per state"),
                             dcc.Graph(
                                 id="main_graph",

                             ),
                         ],

                         ),
            ],
                open=True,
            ),
        ])


def div_barchart(name):
    """Generates an html Div containing graph and control options for smoothing and display, given the name"""
    return html.Div(
        [
            html.Details([
                html.Summary("Nombre avis/ordre par annee ( Bar Chart) "),

                html.Div(id='barchart'),
            ],
                open=True,
            ),
        ])


def div_cumulativ(name):
    """Generates an html Div containing graph and control options for smoothing and display, given the name"""
    return html.Div(
        [
            html.Details(
                [
                    html.Summary('Nombre Avis Traitée Par Année'),

                    dcc.Graph(
                        id="cumul_graph",

                    ),
                ],
                open=True,
            ),
        ])


app.layout = html.Div([
    # Banner display
    html.Div([
        html.H2(
            'Indicateurs MTCE',
            id='title'
        ),
        html.Img(
            src="http://www.hydroquebec.com/images2016/logo-hydro-quebec-coupe.svg"
        )
    ],
        className="banner"
    ),

    # html.Div(generate_table(new)),

    # Body
    html.Div(id='dark-theme-provider-demo', children=[

        dcc.Interval(
            id="interval-log-update",
            n_intervals=0
        ),
        html.Div([
            # Hidden Div Storing JSON-serialized dataframe of run log
            html.Div(id='run-log-storage', style={'display': 'none'}),

            # The html divs storing the graphs and display parameters

            html.Div([

                div_barchart('barchart'),
                div_cumulativ('cumlativ'),
                div_graph('main'),



            ],
                className="ten columns"
            ),


            html.Div([

                html.Div([
                    daq.ToggleSwitch(
                        id='daq-light-dark-theme',
                        label=['Light   ', 'Dark'],
                        value=False,
                        style={'margin-top': '20px'},
                    ),

                    html.Hr(),
                    daq.ToggleSwitch(
                        id='barmode',
                        label=['Variable', 'Stack'],
                        value=False,
                        style={'margin-top': '20px'},
                    ),
                # daq.ToggleSwitch(
                #     id='tech-typ',
                #     label=['Type ordre', 'Technicien'],
                #     value=False,
                #     style={'margin-top': '20px'},
                # ),
                    html.P("Type d'ordre:", style={
                        'font-weight': 'bold', 'margin-bottom': '5px', 'margin-top': '20px'}),
                    dcc.Dropdown(
                        id='type-ordre',
                        options=[{'label': typ, 'value': typ} for typ in TYP],
                        value='D3-ANOI_IPOT',
                        className='twelve columns',
                        multi=True,
                        searchable=True
                    ),


                ],
                    id='type',
                    className='row'
                ),

                html.Div([
                    html.P("Codage:", style={
                        'font-weight': 'bold', 'margin-bottom': '10px'}),

                    dcc.Checklist(
                        options=[
                            {'label': ' R01-R05', 'value': 'R5'},
                            {'label': ' R06-R10', 'value': 'R10'},
                        ],
                        values='',
                        id=f'codage-options'
                    )
                ],
                    style={'margin-top': '10px', 'margin-bottom': '20px'},
                    id='codage'
                ),



                html.Div([
                    html.P("Frequence:", style={
                        'font-weight': 'bold', 'margin-bottom': '10px'}),

                    dcc.RadioItems(
                        options=[
                            {'label': ' Par Annee', 'value': 'AS'},
                            {'label': ' Par Mois', 'value': 'M'}
                        ],
                        value='AS',
                        id=f'frequence-options'
                    )
                ],
                    style={'margin-top': '10px', 'margin-bottom': '20px'},
                    id='frequence'
                ),

                dcc.RangeSlider(
                    marks={i: '{}'.format(i) for i in range(2012, 2019)},
                    min=2012,
                    max=2019,
                    value=[2017, 2019],
                    id='range',
                ),

                html.Hr(),


                html.Div([
                    html.P("Trier par:", style={
                        'font-weight': 'bold', 'margin-bottom': '10px'}),

                    dcc.RadioItems(
                        options=[{'label': k, 'value': k}
                                 for k in namess.keys()],
                        value='Division',
                        style={'margin-top': '10px', 'margin-bottom': '10px'},
                        id=f'filtre'
                    ),


                    dcc.Dropdown(
                        id='choix',
                        # value='0150',
                        className='twelve columns',
                        multi=True,
                        style={'margin-bottom': '40px'},
                        searchable=True
                    ),
                    # html.Button('Telecharger Les donnees',
                    # id='button',
                    # download="NOM_DU_FICHIER_CSV.csv",
                    # href="data:text/csv;charset=iso-8859-1," + urllib.parse.quote(df.to_csv(index=False, sep=';', encoding='iso-8859-1').encode('iso-8859-1')),
                    # target="_blank",
                    # style={'margin-top': '20px', 'display': 'block'},
                    # ),

                    # html.A(
                    #     'Télécharger les ordres/avis',
                    #     id='download_link',
                    #     download="DONNEES.csv",
                    #     href="data:text/csv;charset=iso-8859-1," + urllib.parse.quote(
                    #         df.to_csv(index=False, sep=';', encoding='iso-8859-1').encode('iso-8859-1')),
                    #     target="_blank"
                    # ),
                    html.A('Download CSV', id = 'my-link'),

                    daq.Knob(
                        id='my-daq-knob',
                        value=8,
                        max=10,
                        min=0
                    ),


                ],

                    style={'margin-top': '10px'},
                    id='div-interval-control',
                    className='row'
                ),


            ],
                className="two columns sticky",
                style={'border-left:': '10px', 'margin-top': '20px'}
            ),

            dash_table.DataTable(id='datatable-upload-container'),

        ],
            className="row"
        ),

    ],
        className="container",

    ),

    html.Div(id='df_graph', style={'display': 'none'}
             ),
    html.Div(id='dff_graph', style={'display': 'none'}),
    html.Div(id='output-data-upload', style={'display': 'none'}),



])


# def parse_contents(contents, filename,date):
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    print(contents, 'filename', filename)
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode("ISO-8859-1")), encoding="ISO-8859-1", sep=';')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),
                               encoding="ISO-8859-1", sep=';')
    except Exception as e:
        print(e)

    return df.to_json(date_format='iso', orient='split')


def overwrite_color(data):
    for serie in data:
        if 'R5' in serie['name']:
            serie['marker']['color'] = 'rgb(52, 235, 204)'
        elif 'R10' in serie['name']:
            serie['marker']['color'] = 'rgb(189, 52, 235)'
        elif 'D2' in serie['name']:
            serie['marker']['color'] = 'rgb(139,0,0)'
        elif 'D3-AUTRE' in serie['name']:
            serie['marker']['color'] = 'rgb(255,127,80)'
        elif 'D4' in serie['name']:
            serie['marker']['color'] = 'rgb(44,160,44)'
        elif 'D9' in serie['name']:
            serie['marker']['color'] = 'rgb(255,69,0)'
        elif 'D3-ANOI' in serie['name']:
            serie['marker']['color'] = 'rgb(255,215,0)'
        elif 'D3-IPOT' in serie['name']:
            serie['marker']['color'] = 'rgb(127,255,0)'
        elif 'D3-ANIF' in serie['name']:
            serie['marker']['color'] = 'rgb(0,250,154)'
        elif 'ZDC7-443-Autre' in serie['name']:
            serie['marker']['color'] = 'rgb(75,0,130)'
        elif 'ZDC7-443-Diagnostic' in serie['name']:
            serie['marker']['color'] = 'rgb(255,20,147)'
        elif 'D3' in serie['name']:
            serie['marker']['color'] = 'rgb(210,105,30)'

    return data


@app.callback(Output('my-link', 'href'), [Input('df_graph', 'children')])
def update_link(value):
    return '/dash/urlToDownload?value={}'.format(value)

@app.server.route('/dash/urlToDownload')
def download_csv():
    value = flask.request.args.get('value')
    # create a dynamic csv or file here using `StringIO`
    # (instead of writing to the file system)
    strIO = StringIO.StringIO()
    strIO.write('You have selected {}'.format(value))
    strIO.seek(0)
    return send_file(strIO,
                     mimetype='text/csv',
                     attachment_filename='downloadFile.csv',
                     as_attachment=True)
@app.callback(
    dash.dependencies.Output('choix', 'options'),
    [dash.dependencies.Input('filtre', 'value')]
)
def update_date_choice(name):
    return [{'label': i, 'value': i} for i in namess[name]]


@app.callback(
    Output('dark-theme-provider-demo', 'style'),
    [Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
    if(dark_theme):
        return {'background-color': '#303030', 'color': 'white', 'plot_bgcolor': '#303030', 'paper_bgcolor': '#303030'}
    else:
        return {'background-color': 'white', 'color': 'black'}


@app.callback(Output('df_graph', 'children'),
              [
    # Input('daq-light-dark-theme', "value"),
    Input('type-ordre', "value"),
    Input('frequence-options', "value"),
    Input('choix', "value"),
    Input('filtre', "value"),
    Input('range', 'value'),
    Input('codage-options', 'values') ]
)
def maj_graph(type_ordre, freq, choix, filtre, date,codage):
    global df
    dff = new.copy()

    try:
        if (len(type_ordre) != 0):
            dff = dff[dff['TYPE_CODE'].isin(type_ordre)]
        if (len(choix) != 0) and (filtre == 'Technicien'):
            dff = dff[dff['Technicien'].isin(choix)]
        elif (len(choix) != 0) and (filtre == 'Division'):
            dff = dff[dff['DIV'].isin(choix)]
        elif (len(choix) != 0) and (filtre == 'Territoire'):
            dff = dff[dff['Territoires'].isin(choix)]

    except:
        print('if error')


    if (len(codage) == 0):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['R10','R5']))]
        print("Aucun des Choix ", codage)
    elif "R10" in codage and (len(codage) == 1):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['R5','ZDC7']))]
        print("Choix  de codage R10",codage)
    elif "R5" in codage and (len(codage) == 1):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['R10','ZDC7']))]
        print("Choix  de codage R5 ",codage)
    elif (len(codage) == 2):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['ZDC7']))]
        print("Choix  des 3 courbe", codage)




    dfgraph = pd.pivot_table(dff, index=pd.Grouper(
        key='date', freq=freq), columns=['TYP'], aggfunc='size').fillna(0)


    if len(dfgraph) > 0:

        dfgraph = dfgraph.reindex(pd.DatetimeIndex(
            start=dfgraph.index.min(), end=dfgraph.index.max(), freq=freq))

    lst_champs = []
    for col in dfgraph.columns.tolist():
        if 'confirmes' in col:
            dfgraph[col] = -1 * dfgraph[col]
            lst_champs.append(col.replace('-confirmes', ""))


    for type_code in lst_champs:
        dfgraph[type_code + '-cumul'] = dfgraph[type_code +
                                                '-lances'] + dfgraph[type_code + '-confirmes']
        dfgraph[type_code + '-cumul'] = dfgraph[type_code + '-cumul'].cumsum()

    try:
        if (len(date) != 0):
            dfgraph = dfgraph[(dfgraph.index.year >= date[0]) &
                              (dfgraph.index.year <= date[1])]
            dfgraph = dfgraph.loc[date[0]:date[1]]
            print('DATE', dff)
    except:
        print('date error')
    # df=dfgraph
    # print("VOICIIII le Df:",df)
    return dfgraph.to_json(date_format='iso', orient='split')


@app.callback(Output('dff_graph', 'children'),
              [
    Input('type-ordre', "value"),
    Input('frequence-options', "value"),
    Input('choix', "value"),
    Input('filtre', "value"),
    Input('range', 'value'),
    Input('codage-options', 'values')  ]
)
def majj_graph(type_ordre, freq, choix, filtre, date,codage):

    dff = new.copy()
    try:
        if (len(type_ordre) != 0):

            dff = dff[dff['TYPE_CODE'].isin(type_ordre)]
            # print('preeeeemoiieeeeeeerrr', dff)

        if (len(choix) != 0) and (filtre == 'Technicien'):

            dff = dff[dff['Technicien'].isin(choix)]

        elif (len(choix) != 0) and (filtre == 'Division'):

            dff = dff[dff['DIV'].isin(choix)]

        elif (len(choix) != 0) and (filtre == 'Territoire'):

            dff = dff[dff['Territoires'].isin(choix)]

    except:
        print('if error')

    if (len(codage) == 0):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['R10','R5']))]
        print("Aucun des Choix ", codage)
    elif "R10" in codage and (len(codage) == 1):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['R5','ZDC7']))]
        print("Choix  de codage R10",codage)
    elif "R5" in codage and (len(codage) == 1):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['R10','ZDC7']))]
        print("Choix  de codage R5 ",codage)
    elif (len(codage) == 2):
        dff = dff[~dff['TYP'].fillna('').str.contains('|'.join(['ZDC7']))]
        print("Choix  des 3 courbe", codage)


    if (len(date) != 0):
        dff = dff[(dff.date.dt.year >= date[0])
                  & (dff.date.dt.year <= date[1])]

    dfi = dff.groupby(['latitude', 'longitude'])['TYP'].agg(['count'])

    dfi.reset_index(inplace=True)


    return dfi.to_json(date_format='iso', orient='split')


@app.callback(Output('barchart', 'children'),
              [Input('df_graph', 'children'),
               Input('daq-light-dark-theme', "value"),
               Input('barmode', "value")]
              )
def maj_graph(jsonified_data, dark_theme, bar_mode):
    layout_individuall = copy.deepcopy(layoutt)
    dfgraph = pd.read_json(jsonified_data, orient='split')
    dfgraph = dfgraph[dfgraph.columns[~dfgraph.columns.str.contains(
        'cumul')].tolist()]
    # dfgraph = dfgraph[dfgraph.columns[~dfgraph.columns.str.contains('cumul')].tolist()]
    if(dark_theme):
        layout_individuall['plot_bgcolor'] = '#303030'
        layout_individuall['paper_bgcolor'] = '#303030'
        layout_individuall['font'] = dict(color='#CCCCCC')
        print('white')
    else:

        layout_individuall['plot_bgcolor'] = 'white'
        layout_individuall['paper_bgcolor'] = 'white'
        layout_individuall['font'] = dict(color='black')
        print('black')
    if(bar_mode):
        layout_individuall["barmode"] = 'stack'

    else:
        layout_individuall["barmode"] = 'group'


    data = []
    marginBottom = 100
    marginLeft = 60

    for col in dfgraph.columns.tolist():
        data.append(
            # go.Scatter(
            go.Bar(
                x=dfgraph.index.tolist(),
                # x=(dfgraph.index - offset).tolist(),
                y=dfgraph[col].tolist(),
                # mode = 'lines+markers',
                name=col
            )
        )
        data = overwrite_color(data)

    layout = go.Layout(
        # barmode='stack',
        title='Nb lancés (en haut) et confirmés (en bas)',
        # legend=dict(orientation='h', x=-.1, y=1.2),
        autosize=True,
        # width=500,
        height=800,
        margin=go.Margin(
            l=marginLeft,
            # r=50,
            b=marginBottom,
            # t=0,
            pad=4
        ),
    )

    return dcc.Graph(
        id='graph1_',
        figure={
            'data': data,
            'layout': layout_individuall
        })


@app.callback(Output('cumul_graph', 'figure'),
              [Input('daq-light-dark-theme', "value"),
               Input('df_graph', 'children')])
def make_cumul(dark_theme, jsonified_data):

    layout_individual = copy.deepcopy(layout)
    dfgraph = pd.read_json(jsonified_data, orient='split')
    dfgraph = dfgraph[dfgraph.columns[dfgraph.columns.str.contains(
        'cumul')].tolist()]

    if(dark_theme):
        layout_individual['plot_bgcolor'] = '#303030'
        layout_individual['paper_bgcolor'] = '#303030'
        layout_individual['font'] = dict(color='#CCCCCC')

    else:

        layout_individual['plot_bgcolor'] = 'white'
        layout_individual['paper_bgcolor'] = 'white'
        layout_individual['font'] = dict(color='black')

    data = []

    for col in dfgraph.columns.tolist():
        print(col)
        data.append(
            # go.Scatter(
            dict(
                type='scatter',
                mode='lines+markers',
                name=col,
                x=dfgraph.index.tolist(),
                y=dfgraph[col].tolist(),
                line=dict(
                    shape="spline",
                    smoothing=2,
                    width=1,

                ),
                marker=dict(symbol='diamond-open')
            )
        )
        data = overwrite_color(data)

    layout_individual['title'] = 'Individual Production: '  # noqa: E501

    figure = dict(data=data, layout=layout_individual)
    return figure


@app.callback(Output('main_graph', 'figure'),
              [Input('daq-light-dark-theme', "value"),
               Input('dff_graph', 'children'),
               Input('my-daq-knob', 'value')],
               [State('main_graph', 'relayoutData')])
def map(dark_theme, json, taille,relayout_data):
    layout_individual = copy.deepcopy(layout_map)

    dfi = pd.read_json(json, orient='split')

    if 'xaxis.range[0]' in relayout_data:
        layout_individual['xaxis']['range'] = [
            relayout_data['xaxis.range[0]'],
            relayout_data['xaxis.range[1]']
        ]
        print("ZOOOMMMMMMMM RANGe",layout_individual['xaxis'])

    if 'yaxis.range[0]' in relayout_data:
        layout_individual['yaxis']['range'] = [
            relayout_data['yaxis.range[0]'],
            relayout_data['yaxis.range[1]']
        ]

    if(dark_theme):
        layout_individual['plot_bgcolor'] = '#303030'
        layout_individual['paper_bgcolor'] = '#303030'
        layout_individual['font'] = dict(color='#CCCCCC')

    else:

        layout_individual['plot_bgcolor'] = 'white'
        layout_individual['paper_bgcolor'] = 'white'
        layout_individual['font'] = dict(color='black')
    dfi['tile'] = dfi['count'] / (10/taille*100 )
    # print('mappp datttaaa', dfi)

    data = [
        go.Scattermapbox(
            lat=dfi['longitude'].tolist(),
            lon=dfi['latitude'].tolist(),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=dfi['tile'].tolist(),
            ),
            text=dfi['count'].tolist(),
        )
    ]

    figure = dict(data=data, layout=layout_individual)
    return figure


app.css.append_css(
    {"external_url": "https://codepen.io/mrrobotsca/pen/ywyvLL.css"})

################################################
# app.config.update({'routes_pathname_prefix': '',
#                    'requests_pathname_prefix': ''})
# Running the server
if __name__ == '__main__':
    app.run_server(debug=True)
