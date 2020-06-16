# -*- coding: utf-8 -*-
"""
Module doc string
"""
import pathlib
import re
import json
from datetime import datetime
import flask
import dash
import dash_table
import matplotlib.colors as mcolors
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import copy
import numpy as np
from precomputing import add_stopwords
from dash.dependencies import Output, Input, State
from dateutil import relativedelta
from wordcloud import WordCloud, STOPWORDS
from ldacomplaints import lda_analysis
from sklearn.manifold import TSNE
import pandas as pd
layoutt = dict(
    autosize=True,
    height=800,
    barmode='stack',
    template="plotly_white",
    font=dict(color='#000000'),
    titlefont=dict(color='#000000', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    # plot_bgcolor="#191A1A",
    # paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Cumulatif - Nb lancés (en haut) et confirmés (en bas)',
)
data_df = pd.read_csv('new_cases.csv')
data_df2= pd.read_csv('DATAFRAME.csv')
result=pd.DataFrame()

countires=data_df.columns[data_df.columns.isin(data_df2["location"])]

countires=data_df.columns[data_df.columns.isin(data_df2["location"])].tolist()

countires.append('date')


embed_df = pd.read_csv(
    "data/tsne_bigram_data.csv", index_col=0
)  # Bigram embedding dataframe, with placeholder tsne values (at perplexity=3)
vects_df = pd.read_csv(
    "data/bigram_vectors.csv", index_col=0
)  # Simple averages of GLoVe 50d vectors
bigram_df = pd.read_csv("data/bigram_counts_data.csv", index_col=0)

DATA_PATH = pathlib.Path(__file__).parent.resolve()
EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
FILENAME = "data/customer_complaints_narrative_sample.csv"
FILENAME_PRECOMPUTED = "data/precomputed.json"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
GLOBAL_DF = pd.read_csv(DATA_PATH.joinpath(FILENAME), header=0)
with open(DATA_PATH.joinpath(FILENAME_PRECOMPUTED)) as precomputed_file:
    PRECOMPUTED_LDA = json.load(precomputed_file)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for Heroku deployment

# app.layout = html.Div(children=[NAVBAR, BODY])

"""
#  Callbacks
"""

"""
We are casting the whole column to datetime to make life easier in the rest of the code.
It isn't a terribly expensive operation so for the sake of tidyness we went this way.
"""
GLOBAL_DF["Date received"] = pd.to_datetime(
    GLOBAL_DF["Date received"], format="%m/%d/%Y"
)

"""
In order to make the graphs more useful we decided to prevent some words from being included
"""
ADDITIONAL_STOPWORDS = [
    "XXXX",
    "XX",
    "xx",
    "xxxx",
    "n't",
    "Trans Union",
    "BOA",
    "Citi",
    "account",
]
for stopword in ADDITIONAL_STOPWORDS:
    STOPWORDS.add(stopword)



def sample_data(dataframe, float_percent):

    print("making a local_df data sample with float_percent: %s" % (float_percent))
    return dataframe.sample(frac=float_percent, random_state=1)

def data(pays):
    countires.append('date')
    data_df3=data_df[countires]
    count_fakes=data_df2[data_df2['location'] == pays].groupby(['date']).count().drop(['location', 'verifier'], axis = 1)
    # print(count_fakes)
    count_fakes.index=pd.to_datetime(count_fakes.index).date
    data_df3['date']=pd.to_datetime(data_df3['date'])
    data_df3=data_df3[['date',pays]][data_df3['date'].isin(count_fakes.index.tolist())]
    count_fakes = count_fakes.loc[:, ~count_fakes.columns.str.contains('^Unnamed')]
    count_fakes.index=count_fakes.index.rename('date')
    # print(count_fakes)
    data_df3=data_df3.set_index('date')
    result = pd.concat([data_df3, count_fakes], axis=1,  join='inner')
    result[pays] = result[pays]/1000
    result['fakenews'] = result['fakenews']*-1
    return result

def get_complaint_count_by_company(dataframe):
    """ Helper function to get complaint counts for unique banks """
    company_counts = dataframe["Company"].value_counts()
    # we filter out all banks with less than 11 complaints for now
    company_counts = company_counts[company_counts > 10]
    values = company_counts.keys().tolist()
    counts = company_counts.tolist()
    return values, counts


def calculate_bank_sample_data(dataframe, sample_size, time_values):
    """ TODO """
    print(
        "making bank_sample_data with sample_size count: %s and time_values: %s"
        % (sample_size, time_values)
    )
    if time_values is not None:
        min_date = time_values[0]
        max_date = time_values[1]
        dataframe = dataframe[
            (dataframe["Date received"] >= min_date)
            & (dataframe["Date received"] <= max_date)
        ]
    company_counts = dataframe["Company"].value_counts()
    company_counts_sample = company_counts[:sample_size]
    values_sample = company_counts_sample.keys().tolist()
    counts_sample = company_counts_sample.tolist()

    return values_sample, counts_sample


def make_local_df(selected_bank, time_values, n_selection):
    """ TODO """
    print("redrawing bank-wordcloud...")
    n_float = float(n_selection / 100)
    print("got time window:", str(time_values))
    print("got n_selection:", str(n_selection), str(n_float))
    # sample the dataset according to the slider
    local_df = sample_data(GLOBAL_DF, n_float)
    if time_values is not None:
        time_values = time_slider_to_date(time_values)
        local_df = local_df[
            (local_df["Date received"] >= time_values[0])
            & (local_df["Date received"] <= time_values[1])
        ]
    if selected_bank:
        local_df = local_df[local_df["Company"] == selected_bank]
        add_stopwords(selected_bank)
    return local_df


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

def make_marks_time_slider(mini, maxi):
    """
    A helper function to generate a dictionary that should look something like:
    {1420066800: '2015', 1427839200: 'Q2', 1435701600: 'Q3', 1443650400: 'Q4',
    1451602800: '2016', 1459461600: 'Q2', 1467324000: 'Q3', 1475272800: 'Q4',
     1483225200: '2017', 1490997600: 'Q2', 1498860000: 'Q3', 1506808800: 'Q4'}
    """
    step = relativedelta.relativedelta(months=+1)
    start = datetime(year=mini.year, month=1, day=1)
    end = datetime(year=maxi.year, month=maxi.month, day=30)
    ret = {}

    current = start
    while current <= end:
        current_str = int(current.timestamp())
        if current.month == 1:
            ret[current_str] = {
                "label": str(current.year),
                "style": {"font-weight": "bold"},
            }
        elif current.month == 4:
            ret[current_str] = {
                "label": "Q2",
                "style": {"font-weight": "lighter", "font-size": 7},
            }
        elif current.month == 7:
            ret[current_str] = {
                "label": "Q3",
                "style": {"font-weight": "lighter", "font-size": 7},
            }
        elif current.month == 10:
            ret[current_str] = {
                "label": "Q4",
                "style": {"font-weight": "lighter", "font-size": 7},
            }
        else:
            pass
        current += step
    # print(ret)
    return ret



def time_slider_to_date(time_values):
    """ TODO """
    min_date = datetime.fromtimestamp(time_values[0]).strftime("%c")
    max_date = datetime.fromtimestamp(time_values[1]).strftime("%c")
    print("Converted time_values: ")
    print("\tmin_date:", time_values[0], "to: ", min_date)
    print("\tmax_date:", time_values[1], "to: ", max_date)
    return [min_date, max_date]


def make_options_bank_drop(values):
    """
    Helper function to generate the data format the dropdown dash component wants
    """
    ret = []
    for value in values:
        ret.append({"label": value, "value": value})
    return ret


def populate_lda_scatter(tsne_df, df_top3words, df_dominant_topic):
    """Calculates LDA and returns figure data you can jam into a dcc.Graph()"""
    mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])

    # for each topic we create a separate trace
    traces = []
    for topic_id in df_top3words["topic_id"]:
        tsne_df_f = tsne_df[tsne_df.topic_num == topic_id]
        cluster_name = ", ".join(
            df_top3words[df_top3words["topic_id"] == topic_id]["words"].to_list()
        )
        trace = go.Scatter(
            name=cluster_name,
            x=tsne_df_f["tsne_x"],
            y=tsne_df_f["tsne_y"],
            mode="markers",
            hovertext=tsne_df_f["doc_num"],
            marker=dict(
                size=6,
                color=mycolors[tsne_df_f["topic_num"]],  # set color equal to a variable
                colorscale="Viridis",
                showscale=False,
            ),
        )
        traces.append(trace)

    layout = go.Layout({"title": "Topic analysis using LDA"})

    return {"data": traces, "layout": layout}


def plotly_wordcloud(data_frame):
    """A wonderful function that returns figure data for three equally
    wonderful plots: wordcloud, frequency histogram and treemap"""
    complaints_text = list(data_frame["Consumer complaint narrative"].dropna().values)

    if len(complaints_text) < 1:
        return {}, {}, {}

    # join all documents in corpus
    text = " ".join(list(complaints_text))

    word_cloud = WordCloud(stopwords=set(STOPWORDS), max_words=100, max_font_size=90)
    word_cloud.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 450],
            },
            "margin": dict(t=20, b=20, l=10, r=10, pad=4),
            "hovermode": "closest",
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}
    word_list_top = word_list[:25]
    word_list_top.reverse()
    freq_list_top = freq_list[:25]
    freq_list_top.reverse()

    frequency_figure_data = {
        "data": [
            {
                "y": word_list_top,
                "x": freq_list_top,
                "type": "bar",
                "name": "",
                "orientation": "h",
            }
        ],
        "layout": {"height": "550", "margin": dict(t=20, b=20, l=100, r=20, pad=4)},
    }
    treemap_trace = go.Treemap(
        labels=word_list_top, parents=[""] * len(word_list_top), values=freq_list_top
    )
    treemap_layout = go.Layout({"margin": dict(t=10, b=10, l=5, r=5, pad=4)})
    treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}
    return wordcloud_figure_data, frequency_figure_data, treemap_figure


"""
#  Page layout and contents

In an effort to clean up the code a bit, we decided to break it apart into
sections. For instance: LEFT_COLUMN is the input controls you see in that gray
box on the top left. The body variable is the overall structure which most other
sections go into. This just makes it ever so slightly easier to find the right
spot to add to or change without having to count too many brackets.
"""

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("AI Project 2020", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)


LDA_PLOT = dcc.Loading(
    id="loading-lda-plot", children=[dcc.Graph(id="tsne-lda")], type="default"
)
LDA_TABLE = html.Div(
    id="lda-table-block",
    children=[
        dcc.Loading(
            id="loading-lda-table",
            children=[
                dash_table.DataTable(
                    id="lda-table",
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "Text"},
                            "textAlign": "left",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "min-width": "50%",
                        }
                    ],
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgb(243, 246, 251)",
                        }
                    ],
                    style_cell={
                        "padding": "16px",
                        "whiteSpace": "normal",
                        "height": "auto",
                        "max-width": "0",
                    },
                    style_header={"backgroundColor": "white", "fontWeight": "bold"},
                    style_data={"whiteSpace": "normal", "height": "auto"},
                    filter_action="native",
                    page_action="native",
                    page_current=0,
                    page_size=5,
                    columns=[],
                    data=[],
                )
            ],
            type="default",
        )
    ],
    style={"display": "none"},
)

LDA_PLOTS = [
    dbc.CardHeader(html.H5("Topic modelling using LDA")),
    dbc.Alert(
        "Not enough data to render LDA plots, please adjust the filters",
        id="no-data-alert-lda",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            html.P(
                "Click on a complaint point in the scatter to explore that specific complaint",
                className="mb-0",
            ),
            html.P(
                "(not affected by sample size or time frame selection)",
                style={"fontSize": 10, "font-weight": "lighter"},
            ),
            LDA_PLOT,
            html.Hr(),
            LDA_TABLE,
        ]
    ),
]
WORDCLOUD_PLOTS = [
    dbc.CardHeader(html.H5("Most frequently used words in complaints")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
    [

        dcc.Tabs(
                id="tabs",
                children=[
                    dcc.Tab(
                        label="Treemap",
                        children=[
                            dcc.Loading(
                                id="loading-treemap",
                                children=[dcc.Graph(id="bank-treemap")],
                                type="default",
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Wordcloud",
                        children=[
                            dcc.Loading(
                                id="loading-wordcloud",
                                children=[
                                    dcc.Graph(id="bank-wordcloud")

                                ],
                                type="default",
                            ),
                            html.Img(src=app.get_asset_url('svg.svg'), style={
                    'height' : '200%',
                    'width' : '200%',
                    'float' : 'right',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-right' : 0
                })
                        ],
                    ),
                ],
            )

        ]
    ),
]

TOP_BANKS_PLOT = [

]

TOP_BIGRAM_PLOT = [
    # dbc.CardHeader(html.H5("Top bigrams found in the database")),
    html.Div(id='barchart'),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-scatter",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P(["Choose a t-SNE perplexity value:"]), md=6),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="bigrams-perplex-dropdown",
                                        options=[
                                            {"label": str(i), "value": i}
                                            for i in range(3, 7)
                                        ],
                                        value=3,
                                    )
                                ],
                                md=3,
                            ),
                        ]
                    ),
                    dcc.Graph(id="bigrams-scatter"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

TOP_BIGRAM_COMPS = [
    dbc.CardHeader(html.H5("Comparing Amount of Fakes News Data vs New COVID cases")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Choose countires"), md=12),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="bigrams-comp_1",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in countires
                                        ],
                                        value="India",
                                    )
                                ],
                                md=6,
                            )
                            
                        ]
                    ),
                    # dcc.Graph(id="bigrams-comps"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

TOP_WCLOUD_PLOT = [
    dbc.CardHeader(html.H5("Word Clouds")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-scatterr",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="word-clouds",
                        color="warning",
                        style={"display": "none"},
                    ),

                    html.Img(src=app.get_asset_url('svg.svg'))
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container(
    
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_WCLOUD_PLOT)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_PLOT)),], style={"marginTop": 30}),
        dbc.Card(WORDCLOUD_PLOTS),
        dbc.Row([dbc.Col([dbc.Card(LDA_PLOTS)])], style={"marginTop": 50}),
    ],
    className="mt-12",
)



app.layout = html.Div(children=[NAVBAR, BODY])
# countires.append('date')
# data_df3=data_df[countires]

def data(pays):
    countires.append('date')
    data_df3=data_df[countires]
    count_fakes=data_df2[data_df2['location'] == pays].groupby(['date']).count().drop(['location', 'verifier'], axis = 1)
    # print(count_fakes)
    count_fakes.index=pd.to_datetime(count_fakes.index).date
    data_df3['date']=pd.to_datetime(data_df3['date'])
    data_df3=data_df3[['date',pays]][data_df3['date'].isin(count_fakes.index.tolist())]
    count_fakes = count_fakes.loc[:, ~count_fakes.columns.str.contains('^Unnamed')]
    count_fakes.index=count_fakes.index.rename('date')
    # print(count_fakes)
    data_df3=data_df3.set_index('date')
    result = pd.concat([data_df3, count_fakes], axis=1,  join='inner')
    result[pays] = result[pays]/1000
    result['fakenews'] = result['fakenews']*-1
    return result

# data()
@app.callback(
    Output("bigrams-scatter", "figure"), [Input("bigrams-perplex-dropdown", "value")],
)
def populate_bigram_scatter(perplexity):
    X_embedded = TSNE(n_components=2, perplexity=perplexity).fit_transform(vects_df)

    embed_df["tsne_1"] = X_embedded[:, 0]
    embed_df["tsne_2"] = X_embedded[:, 1]
    fig = px.scatter(
        embed_df,
        x="tsne_1",
        y="tsne_2",
        hover_name="bigram",
        text="bigram",
        size="count",
        color="words",
        size_max=45,
        template="plotly_white",
        title="Bigram similarity and frequency",
        labels={"words": "Avg. Length<BR>(words)"},
        color_continuous_scale=px.colors.sequential.Sunsetdark,
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="Gray")))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig




# result= data()
# @app.callback(
#     Output("bigrams-comps", "figure"),
#     [Input("bigrams-comp_1", "value")]
# )
# def comp_bigram_comparisons(comp_first):
#     # comp_list = [comp_first, comp_second]
#     # temp_df = bigram_df[bigram_df.company.isin(comp_list)]
#     # temp_df.loc[temp_df.company == comp_list[-1], "value"] = -temp_df[
#     #     temp_df.company == comp_list[-1]
#     # ].value.values
    
#     print(result)
#     data = []
#     marginBottom = 100
#     marginLeft = 60

#     for col in result.columns.tolist():
#         print(col)
#         data.append(
#             # go.Scatter(
#             go.Bar(
#                 x=result.index.tolist(),
#                 # x=(dfgraph.index - offset).tolist(),
#                 y=result[col].tolist(),
#                 # mode = 'lines+markers',
#                 name=col
#             )
#         )


#     layout = go.Layout(
#         # barmode='stack',
#         title='Nb lancés (en haut) et confirmés (en bas)',
#         # legend=dict(orientation='h', x=-.1, y=1.2),
#         autosize=True,
#         # width=500,
#         height=800,
#         margin=go.Margin(
#             l=marginLeft,
#             # r=50,
#             b=marginBottom,
#             # t=0,
#             pad=4
#         ),
#     )

#     return dcc.Graph(
#         id='graph1_',
#         figure={
#             'data': data,
#             'layout': layout_individuall
#         })

#     # fig = px.bar(
#     #     result,
#     #     title="Comparison: " + comp_first + " | " + comp_second,
#     #     x="ngram",
#     #     y="value",
#     #     color="company",
#     #     template="plotly_white",
#     #     color_discrete_sequence=px.colors.qualitative.Bold,
#     #     labels={"company": "Company:", "ngram": "N-Gram"},
#     #     hover_data="",
#     # )
#     # fig.update_layout(legend=dict(x=0.1, y=1.1), legend_orientation="h")
#     # fig.update_yaxes(title="", showticklabels=False)
#     # fig.data[0]["hovertemplate"] = fig.data[0]["hovertemplate"][:-14]
#     # return fig


# print(result)




@app.callback(Output('barchart', 'children'),
              [Input("bigrams-comp_1", "value")]
              )
def maj_graph(pays):
    layout_individuall = copy.deepcopy(layoutt)
    layout_individuall["barmode"] = 'group'
    # print(mrd)
    # layout_individuall = copy.deepcopy(layoutt)
    # dfgraph = pd.read_json(jsonified_data, orient='split')
    # dfgraph = dfgraph[dfgraph.columns[~dfgraph.columns.str.contains(
    #     'cumul')].tolist()]
    # # dfgraph = dfgraph[dfgraph.columns[~dfgraph.columns.str.contains('cumul')].tolist()]
    # if(dark_theme):
    #     layout_individuall['plot_bgcolor'] = '#303030'
    #     layout_individuall['paper_bgcolor'] = '#303030'
    #     layout_individuall['font'] = dict(color='#CCCCCC')
    #     print('white')
    # else:

    #     layout_individuall['plot_bgcolor'] = 'white'
    #     layout_individuall['paper_bgcolor'] = 'white'
    #     layout_individuall['font'] = dict(color='black')
    #     print('black')
    # if(bar_mode):
    #     layout_individuall["barmode"] = 'stack'

    # else:
    #     layout_individuall["barmode"] = 'group'
        
    # data()
    data_df = pd.read_csv('new_cases.csv')
    data_df2= pd.read_csv('DATAFRAME.csv')
    print(countires)
    
    data_df3=data_df[countires]
    count_fakes=data_df2[data_df2['location'] == pays].groupby(['date']).count().drop(['location', 'verifier'], axis = 1)
    # print(count_fakes)
    count_fakes.index=pd.to_datetime(count_fakes.index).date
    data_df3['date']=pd.to_datetime(data_df3['date'])
    data_df3=data_df3[['date',pays]][data_df3['date'].isin(count_fakes.index.tolist())]
    count_fakes = count_fakes.loc[:, ~count_fakes.columns.str.contains('^Unnamed')]
    count_fakes.index=count_fakes.index.rename('date')
    # print(count_fakes)
    data_df3=data_df3.set_index('date')
    result = pd.concat([data_df3, count_fakes], axis=1,  join='inner')
    result[pays] = result[pays]/1000
    
    result['fakenews'] = result['fakenews']*-1
    result['fakenews'] = result['fakenews'].rename('FakeNews')
    # result= data(mrd)
    print(result)
    print(layout_individuall)
    data = []
    marginBottom = 100
    marginLeft = 60

    for col in result.columns.tolist():
        print(col)
        data.append(
            # go.Scatter(
            go.Bar(
                x=result.index.tolist(),
                # x=(dfgraph.index - offset).tolist(),
                y=result[col].tolist(),
                # mode = 'lines+markers',
                name=col
            )
        )


    layout = go.Layout(
        # barmode='stack',
        title='Nummber of fake news vs New COVID case (thousands)',
        # legend=dict(orientation='h', x=-.1, y=1.2),
        autosize=True,
        # width=500,
        template="plotly_white",
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


@app.callback(
    [Output("lda-table", "filter_query"), Output("lda-table-block", "style")],
    [Input("tsne-lda", "clickData")],
    [State("lda-table", "filter_query")],
)
def filter_table_on_scatter_click(tsne_click, current_filter):
    """ TODO """
    if tsne_click is not None:
        selected_complaint = tsne_click["points"][0]["hovertext"]
        if current_filter != "":
            filter_query = (
                "({Document_No} eq "
                + str(selected_complaint)
                + ") || ("
                + current_filter
                + ")"
            )
        else:
            filter_query = "{Document_No} eq " + str(selected_complaint)
        print("current_filter", current_filter)
        return (filter_query, {"display": "block"})
    return ["", {"display": "none"}]


# @app.callback(Output("bank-drop", "value"), [Input("bank-sample", "clickData")])
# def update_bank_drop_on_click(value):
#     """ TODO """
#     if value is not None:
#         selected_bank = value["points"][0]["x"]
#         return selected_bank
#     return "EQUIFAX, INC."


if __name__ == "__main__":
    app.run_server(debug=True)
