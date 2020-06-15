"""
Main script for creating the app layout and callbacks
"""

# Importing libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime as dt
from datetime import date
import numpy as np
import datetime

from plotly.graph_objs import *
from dateutil.relativedelta import relativedelta
import warnings
warnings.filterwarnings("ignore")
# Importing dependencies
from download_data import download_data
from data_load import data_ingest
from forecasting import forecast
# from clustering_dataload import initial_data,scatter_data,sunburst_single,sunburst_multi
from utils import unix_time_millis, get_marks_from_start_end, create_divs
import base64

# Downloading the latest data
download_data()
# REading the data for Quantitative dataset
df,countryDays_df,latest_df, country_df,canada_df,sumdf = data_ingest()
# Defining the dataframe versions for visualization
# df-> Countries and provinces with All days
# countryDays_df -> Country Df with all days
# latest_df -> Countries and provinces with latest date
# country_df -> Countries with latest date

# Reading the data for qualitative dataset
# df_covid = initial_data() #Loading Covid Research Database DF


# Some versions of dataframe for global data
latest_df1 = latest_df.sort_values(['Confirmed'], ascending = False)
top_conf_df = country_df.sort_values(['Confirmed'], ascending = False)
top_active_df = country_df.sort_values(['Active'], ascending = False)
top_death_df = country_df.sort_values(['Death'], ascending = False)
top_recovered_df = country_df.sort_values(['Recovered'], ascending = False)

new_df = country_df[['Country/Region','Confirmed','Death','Recovered']]
desc_country_df = country_df.sort_values(['Confirmed'], ascending = False)
countries = desc_country_df["Country/Region"]


# Global Values for the main DIV on tab 1
confirmedVal = '{:,d}'.format(latest_df['Confirmed'].sum())
ActiveVal = '{:,d}'.format(latest_df["Active"].sum())
DeathVal = '{:,d}'.format(latest_df["Death"].sum())
RecoveredVal = '{:,d}'.format(latest_df["Recovered"].sum())
FatalityRate = '{:.2f}'.format(latest_df["Death"].sum()/latest_df['Confirmed'].sum()*100)+"%"
newConfirmedVal = '{:,d}'.format(latest_df['New Confirmed'].sum())
newDeathVal = '{:,d}'.format(latest_df['New Death'].sum())
newRecoveredVal = '{:,d}'.format(latest_df['New Recovered'].sum())
epoch = datetime.datetime.utcfromtimestamp(0)

# Values for Canada Highlights
canadaConfirmed = '{:,d}'.format(canada_df['Confirmed'].sum())
canadaDeath = '{:,d}'.format(canada_df['Death'].sum())
canadaRecovered = '{:,d}'.format(canada_df['Recovered'].sum())
canadaNewConfirmed = '{:,d}'.format(canada_df['New Confirmed'].sum())
canadaNewDeath = '{:,d}'.format(canada_df['New Death'].sum())
canadaNewRecovered = '{:,d}'.format(canada_df['New Recovered'].sum())
canadaFatalityRate = '{:.2f}'.format(canada_df['Death'].sum()/canada_df['Confirmed'].sum()*100) + "%"
canadaCasesPop = '{:.0f}'.format(canada_df['Confirmed'].sum()/canada_df['Population'].sum()*100000)

# Initializing the dropdown options for app layout

target_options = [{'label': i, 'value': i} for i in ['Confirmed', 'Active',
                        'Death','Recovered']] # dropdown option for case type
target_options1 = [{'label': i, 'value': i} for i in ['Confirmed',
                        'Death','Recovered']] # dropdown option for case type

target_options2 = [{'label': i, 'value': i} for i in [
                    'Confirmed','Active','Death','Recovered',
                    'New Confirmed', 'New Death', 'New Recovered']] # dropdown option for case type

target_options3 = [{'label': i, 'value': i} for i in [
                    'New Confirmed', 'New Death', 'New Recovered']] # dropdown option for case type

target_options4 = [{'label': i, 'value': i} for i in [
                    'Confirmed','Active','Death','Recovered','Fatality Rate',
                    'New Confirmed', 'New Death', 'New Recovered']] # dropdown option for case type

top_options =  [{'label': 'Top 20', 'value': 'Top 20'},
                        {'label': 'Top 30', 'value': 'Top 30'}]# dropdown option for top countries

                        # {'label': 'Top 40', 'value': 'Top 40'}]
countries_options = [{'label': 'Top 10', 'value': 'Top 10'},
                        {'label': 'G7', 'value': 'G7'},
                        {'label': 'BRICS', 'value': 'BRICS'}] # dropdown option for top countries

scale_options = [{'label': i, 'value': i} for i in ['Linear', 'Log']] # radio option for y_Axis scale


single_level_options = [{'label': i, 'value': i} for i in ['5 Clusters',
                        '10 Clusters', '15 Clusters']] # dropdown option for number of clusters

multi_level_options = [{'label': i, 'value': i} for i in ['5 Parents-5 Child Clusters',
                        '5 Parents-10 Child Clusters']] # dropdown option for number of parent-child clusters

country_options = [{'label': 'Global', 'value': 'Global'}]  # dropdown option for countries
option_df = latest_df.loc[latest_df['Province/State']!=0]
cols = list(option_df['Country/Region'].unique())
for i in range(len(cols)):
    country_options.append({'label':cols[i],'value':cols[i]})

country_options1 = [{'label': 'Global', 'value': 'Global'}] # dropdown option for countries
cols = list(country_df['Country/Region'])
for i in range(len(cols)):
    country_options1.append({'label':cols[i],'value':cols[i]})

image_filename_1 = './assets/logo_1_ualberta.png' # logo1
encoded_image_1 = base64.b64encode(open(image_filename_1, 'rb').read())

image_filename_2 = './assets/logo_2_mm.png' # logo2
encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())

""" ###################################################
Defining Custom Styling Used in the Application
###################################################"""
template = 'simple_white'
colors = {
    'page_color': '#000000',
    'background': '#75D5FF',
    'bg': '#DCF3FF',
    'text': '#000000',
    'text1':'#000000',
    'text3':'#666666',
    'text2':'#FFFFFF',
    'graph_bg_color':'#FFFFFF',
    'graph_map_color':'#FFFFFF',
    'graph_text':'#000000',
    'div_color1':' #F1F1F1',
    'heading':'#C01414',
    'Confirmed': '#192AB4',
    'Active': '#ff6f00',
    'Death': '#da5657',
    'Recovered': '#16B965',
    'graph_title1':'#C01414',
    'titlebox_border':'thin lightgrey solid',
    'titlebox_background':'#F1F1F1',

}
colorscales = {
'Confirmed': 'portland',
'Active': 'oranges',
'Death': 'reds',
'Recovered':'viridis'
}

title_box = {
    'borderBottom': colors['titlebox_border'],
    'backgroundColor': colors['titlebox_background'],
    'padding': '10px 5px'}
title_box1 = {
    'borderBottom': colors['titlebox_border'],
    'backgroundColor': colors['heading'],
    'padding': '10px 5px'}
break_box = {
    # 'borderBottom': colors['titlebox_border'],
    'backgroundColor': colors['text2'],
    'padding': '10px 5px'}

heading2 = {
    'text-align':'center',
    'font-family':'sans-serif',
    'color': colors["heading"],
    }
heading3 = {
    'text-align':'center',
    'font-family':'sans-serif',
    'color': colors["text2"],
    'font-style':'bold',
    'font-size': '22px',
    }
heading4 = {
    'text-align':'center',
    'color': colors["text2"],
    'font-style':'bold',
    'font-size': '19px',
    }
small_italics = {
'font-style': 'italic',
'text-align':'center',
'font-size': '18px'
}
small_italics1 = {
'font-style': 'italic',
'text-align':'center',
'font-size': '12px'
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'color':'#000000'
}
page_style = {
'overflowY': 'scroll',
'height': 200
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#C01414',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
}
inner_tab_style = {
    'text-align':'center',
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#C01414',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
}
graph_style = {
# 'borderTop': '1px solid #d6d6d6',
# 'borderBottom': '1px solid #d6d6d6',
'padding': '2px',
# 'display': 'inline-block',
# 'box-shadow': '3px 3px 3px 3px lightgrey',
'padding-top':'2px',
'float':'center',
'backgroundColor':colors['graph_bg_color'],
'plot_bgcolor': colors['graph_bg_color']

}
graph_style1 = {
# 'borderTop': '1px solid #d6d6d6',
# 'borderBottom': '1px solid #d6d6d6',
'padding': '2px',
# 'display': 'inline-block',
# 'box-shadow': '3px 3px 3px 3px lightgrey',
'padding-top':'2px',
'float':'center',
'backgroundColor':colors['graph_bg_color'],
'plot_bgcolor': colors['graph_bg_color']

}
div_small_text = {
'font-size': '11px',
'text-align':'center',
'color' : colors['text1']
}
div_small_text1 = {
'font-size': '14px',
'text-align':'center',
'color' : colors['text1'],
'font-style':'italic'
}

it_content = {
'text-align':'center',
'font-family':'sans-serif',
'font-style': 'italic'
}

content = {
'text-align':'center',
'font-family':'sans-serif',
'font-style': 'bold'
}
chart_box = {
  'box-shadow': '3px 3px 3px 3px lightgrey',
  'padding-top':'2px',"width": "900px",
  "margin": "0 auto",
  'backgroundColor':colors['background'],
  'plot_bgcolor': colors['background']
}
chart_box1 = {
  'box-shadow': '3px 3px 3px 3px lightgrey',
  'padding-top':'2px',
  'padding-left':'10px',
  "margin": "5px",
  'backgroundColor':colors['graph_bg_color'],
  'plot_bgcolor': colors['graph_bg_color']
}
overlay = {'opacity':'0.8',
'background-color':'#000000',
'position':'fixed',
'width':'100%',
'height':'100%',
'top':'0px',
'left':'0px',
'z-index':'1000',
'overflowY':'scroll',
'height':500
}
page = {
'overflowY':'scroll',
'height':5000

}

# Mapbox
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
MAPBOX_STYLE = "mapbox://styles/plotlymapbox/cjyivwt3i014a1dpejm5r7dwr"


# Initializing Dash application
app = dash.Dash(__name__)
server = app.server



""" ###################################################
App Layout Creation
###################################################"""
# Creating the app layout
app.layout = html.Div(children=[

    html.Div(children = [
        html.Div([
                 html.Img(src='data:image/png;base64,{}'.format(encoded_image_1.decode()), height = 40)
        ],style = {"position": "absolute", "left": "20px", "align-self": "center"}),
        html.Div([
            html.H2("COVID-19 Dashboard",
            style={'text-align':'center','font-family':'sans-serif','color': colors['text']}),
            html.H5("Asket Kaur | Frincy Clement | Maryam Sedghi",
            style={'text-align':'center','font-family':'sans-serif','color': colors['text3']}),
            html.P("Last Updated on "+ df['Date'].max().strftime('%B %d, %Y'),
            style={'text-align':'center','font-family':'sans-serif','font-style':'italic','font-size':'16px','color': colors['heading']}),
            html.Div([
            html.Label(['Data Source: ', html.A('John Hopkins University', href='https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data', target='_blank')]),
            ],style={'text-align':'center','font-family':'sans-serif','color': colors['text'],'font-style':'italic','font-size':'12px'}),
        ],style={"margin": "auto"}),
        html.Div([
                 html.Img(src='data:image/png;base64,{}'.format(encoded_image_2.decode()), height = 100)
        ],style = {"position": "absolute", "right": "20px", "align-self": "center"}),
    ],style={"display": "flex", "flex-direction": "row"}),

    # html.H2("COVID-19 Dashboard",
    # style={'text-align':'center','font-family':'sans-serif','color': colors['text']}),
    # html.H5("Asket Kaur | Frincy Clement | Maryam Sedghi",
    # style={'text-align':'center','font-family':'sans-serif','color': colors['text3']}),
    # html.P("Last Updated on "+ df['Date'].max().strftime('%B %d, %Y'),
    # style={'text-align':'center','font-family':'sans-serif','font-size':'14px','color': colors['heading']}),
    # html.Div([
    # html.Label(['Data Source: ', html.A('John Hopkins University', href='https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data', target='_blank')]),
    # ],style={'text-align':'center','font-family':'sans-serif','color': colors['text'],'font-style':'italic','font-size':'12px'}),
    # Parent of all tabs
    dcc.Tabs(id="tabs-styled-with-inline",
    value='tab-1',
    children=[
        #<----------------------------- Tab 1---------------------------------->
        dcc.Tab(label='Global Trends',
        value='tab-1',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
        html.Div(
            children=[
            #<------------------------ Part-1 Div Tab 1------------------------------>
            html.Div(
            children = [
                # Left-Panel Div
                html.Div(
                    children = [

                    #Global-Cases-div
                    html.Div(
                    children = [
                    #Global-Confirmed-Cases Div
                    html.Div(
                    children = [
                        html.Div([
                        html.P('Confirmed Cases')],
                        style = {'padding-top': "13px"},
                        className = "GlobalName"),
                        html.Div([html.P(''+confirmedVal)],
                        style = {'color':colors["Confirmed"], 'font-weight':'bold'},
                        className = "GlobalValue")
                    ],
                    className="first",
                    ),
                    #Global-Active-Cases Div
                    html.Div(
                    children = [
                        html.Div([html.P('Active Cases')],
                        className = "GlobalName"),
                        html.Div([html.P(''+ActiveVal)],
                        style = {'color': colors['Active'], 'font-weight': 'bold'},
                        className = "GlobalValue"),
                    ],
                    className="first",
                    ),
                    #Global-Death Div
                    html.Div(
                    children = [
                        html.Div([html.P('Deaths')],
                        className = "GlobalName"),
                        html.Div([html.P(''+DeathVal)],
                        style = {"color": colors['Death'], 'font-weight': 'bold'},
                        className = "GlobalValue"),
                    ],
                    className="first",
                    ),
                    #Global-Recovered Div
                    html.Div(
                    children = [
                        html.Div([html.P('Recovered')],
                        className = "GlobalName"),
                        html.Div([html.P(''+RecoveredVal)],
                        style = {'color':colors['Recovered'], 'font-weight':'bold'},
                        className = "GlobalValue"),
                    ],
                    className="first",
                    ),
                    # Global Fatality Div
                    html.Div(
                    children = [
                        html.Div([html.P('Fatality Rate')],
                        className = "GlobalName"),
                        html.Div([html.P(''+FatalityRate)],
                        style = {'color': colors['Death'], 'font-weight': 'bold'},
                        className = "GlobalValue"),
                    ],
                    className="first",
                    ),
                    # Global New Confirmed cases Div
                    html.Div(
                    children = [
                        html.Div([html.P('New Confirmed Cases')],
                        className = "GlobalName"),
                        html.Div([html.P(''+newConfirmedVal)],
                        style = {'color': colors["text3"], 'font-weight': 'bold'},
                        className = "GlobalValue")
                    ],
                    className="first",
                    ),
                    #Global New Death Div
                    html.Div(
                    children = [
                        html.Div([html.P('New Deaths')],
                        className = "GlobalName"),
                        html.Div([html.P(''+newDeathVal)],
                        style = {"color": colors['text3'], 'font-weight': 'bold'},
                        className = "GlobalValue"),
                    ],
                    className="first",
                    ),
                    #Global New Recovered cases Div
                    html.Div(
                    children = [
                        html.Div([html.P('New Recovered Cases')],
                        className = "GlobalName"),
                        html.Div([html.P(''+newRecoveredVal)],
                        style = {'color': colors['text3'], 'font-weight': 'bold'},
                        className = "GlobalValue"),
                    ],
                    className="first",
                    ),

                    html.Div(style = {"padding":29})
                    ],style={"display": "flex", "flex-direction": "column"},
                    ),# End of Global-Cases div
                ], style = {"height":"100%"},
                className="two columns div-left-panel"), # End-of-Left-Panel

                #Choropleth-Map
                html.Div([

                    # Title Div
                    html.Div([
                        html.H2("Cumulative Figures",
                        style=heading2,
                        className = "container"),
                        html.P("Click the countries on the map to view the country-specific details",
                        style = div_small_text1)
                    ], style= title_box),#End-of-Title-box

                    html.Div(style = {"padding":10}),# For vertical space

                    #Drop-Down-1-Div
                    html.Div([
                        html.P('Select the data to view',
                        style={'text-align':'center','font-family':'sans-serif',
                        'color': colors['text']}),
                        dcc.Dropdown(
                        id='option',
                        options=target_options1,
                        value ='Confirmed',
                        style={'width':'100%',
                        'text-align':'center', 'color':colors["text1"]}
                        ),
                        html.Div(style = {"padding":3}),# For vertical space
                    ], style=title_box,
                    ),#End-of-dropdown

                    html.Div(style = {"padding":3}),# For vertical space

                    #choropleth-Div
                    html.Div([
                        dcc.Graph(
                        id='choropleth',
                        config={'displayModeBar':False},
                        style = {"height":"70vh"},
                        clickData={'points': [{'customdata': ''}]}),
                    ], style = graph_style,
                    className = "twelve columns"),#end-of-choropleth-div

                ], className="seven columns"),#End-of-Choropleth-Map

                #Right-panel
                html.Div(
                    children = [

                    #World/Country Name Div
                    html.Div(id = "type"),

                    # Displaying column values for the right table
                    #Column-Values-Country/Province-Confirmed-Death-Recovered
                    html.Div(
                    children = [
                        html.Div(
                        # First column div
                        children = [
                        html.Div(
                        id = "div-1"),
                        ],style = {'width' : '19vh'},
                        ),
                        html.Div(
                        # Second column Div
                        children = [
                        html.Div(
                        id = "div-2"),
                        ],style = {'width' : '11vh'},
                        ),
                        html.Div( # Third column Div
                        children = [
                        html.Div(
                        id = "div-3"),
                        ],style = {'width' : '11vh'},
                        ),
                        html.Div( # Fourth Column Div
                        children = [
                        html.Div(
                        id = "div-4"),
                        ],style = {'width' : '11vh'},
                        ),
                    ],style={"display": "flex", "flex-direction": "rows",
                    'height':'35vh','overflowY':'scroll','padding-right':'5px'}
                    ),

                    #Vertical-Space
                    html.Div(style = {"padding":15}),

                    # Bar-Chart Div for new cases
                    html.Div([
                        dcc.Graph(id = 'onebar',
                        config={'displayModeBar':False,
                        # 'staticPlot':True,
                        'responsive': True,
                        'doubleClick':False },
                        style = {"height":"40vh"})
                    ],style = {"padding-left":'10px'}),
                ],style = {"height":"100%"},
                className = "special columns div-right-panel"
                ),#End-of-Right-Tab
            ],style={"display": "flex", "flex-direction": "row", "height":"100%", "position":"relative"}),
            #<-----------------------End-of-Part 1 Tab 1-------------------------->

            #<--------------------------Part 2 Div Tab 1-------------------------->
            html.Div(
                children = [

                    # Left-Panel Div
                    html.Div(
                    children = [
                    #Top-7-Countries-Div
                    html.Div(
                    children = [
                        #Div-for-title
                        html.Div([html.P('Top 10 Countries',
                        style= inner_tab_style)]),
                        html.Div(
                        children = [
                        html.Div(id = "top-7")]),
                    ]),#End-of-Top-7-Countries-Div
                    ], style = {"height":"100%"},
                    className="two columns div-left-panel"),#Left-Panel-End

                    #Bubble-Map div
                    html.Div([

                    #Bubble-Map Title Div
                    html.Div([
                        html.H2("Time-Series Animation of Corona Virus Spread",
                        style=heading2,
                        className = "container"),
                        html.P("Click the Play button to animate the map over time ",
                        style = div_small_text1),
                        html.P("Use the slider and hover over map to view the situation on specific date & location",
                        style = div_small_text1)
                        ], style= title_box),

                        #Drop-Down-2-Div
                        html.Div([
                            html.P('Select the data to view'
                            ,style={'text-align':'center','font-family':'sans-serif',
                            'color': colors['text']}),
                            dcc.Dropdown(
                            id='optionbubble',
                            options=target_options,
                            value ='Confirmed',
                            style={'width':'100%',
                            'text-align':'center', 'color':colors["text1"]}
                            ),
                            html.Div(style = {"padding":3}),# For vertical space
                        ], style=title_box),#end-of-dropdown-2

                        #Bubble Map
                        html.Div([
                            dcc.Graph(
                            id='bubblemap',config={'displayModeBar':False},
                            style = {"height":"70vh"}),
                            ],style = graph_style),#End-of-bubble-map-div

                    ],className="seven columns"),#End-of-bubble-map

                    #Right-panel Div
                    html.Div(
                    children = [
                        #Line-Chart div
                        html.Div([
                            dcc.Graph(
                            id = 'oneline',
                            config={'displayModeBar':False,
                                    # 'staticPlot':True,
                                    'responsive': True,
                                    'doubleClick':False },
                            style = {"height":"40vh"})
                        ]),

                        #Vertical-Space
                        html.Div(style = {"padding":10}),

                        #Doughnut-Chart Div
                        html.Div([
                            dcc.Graph(
                            id = 'doughnut',
                            config={'displayModeBar':False},
                            style = {"height":"40vh"})
                        ]),

                        html.Div(style = {"padding":47})

                    ],
                    style = {"height":"100%",'padding-left':'20px','padding-right':'5px'},
                    className = "special columns div-right-panel")
            ],style={"display": "flex", "flex-direction": "row", "height":"100%", "position":"relative"}),
            #<----------------------End-Part-2 Tab 1--------------------------------->
        ],
        style={"display": "flex", "flex-direction": "column"}),#End-ofboth-pages
        ]),
        #<--------------------------End-Tab-1---------------------------------->



        #<----------------------------- Tab 2---------------------------------->
        dcc.Tab(label='Canada Trends',
        value='tab-2',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div(style = {"padding":20}),
            html.Div([
                html.Div(style = {"padding":20}),# For vertical space
                html.Div([ # Title Div for Highlights
                    html.H1("Canada Highlights",
                    style = {'color':colors['text1'],'text-align':'center'})
                    ], style = break_box, className = "twelve columns"),

                html.Div([ # Highlights Values starts here
                    html.Div([
                        html.H3("Total Cases", style = heading3),
                        html.P(canadaConfirmed, style = heading4)
                    ], className = "point columns"),
                    html.Div([
                        html.H3("Total Deaths", style = heading3),
                        html.P(canadaDeath, style = heading4)
                    ], className = "point columns"),
                    html.Div([
                        html.H3("Total Recovered", style = heading3),
                        html.P(canadaRecovered, style = heading4)
                    ], className = "point1 columns"),
                    html.Div([
                        html.H3("New Cases", style = heading3),
                        html.P(canadaNewConfirmed, style = heading4)
                    ], className = "point columns"),
                    html.Div([
                        html.H3("New Deaths", style = heading3),
                        html.P(canadaNewDeath, style = heading4)
                    ], className = "point columns"),
                    html.Div([
                        html.H3("New Recovered", style = heading3),
                        html.P(canadaNewRecovered, style = heading4)
                    ], className = "point1 columns"),
                    html.Div([
                        html.H3("Fatality Rate", style = heading3),
                        html.P(canadaFatalityRate, style = heading4)
                    ], className = "point columns"),
                    html.Div([
                        html.H3("Cases Per 100,000", style = heading3),
                        html.P(canadaCasesPop, style = heading4)
                    ], className = "two columns"),
                ],style = title_box1,className = "twelve columns"),
                # Adding plain vertical space
                html.Div([
                        html.H1("                 ", style = heading3)
                ], style = break_box, className = "twelve columns"),
                # Highlights Div ends here

            html.Div([ # Title for the second part in tab 2
                html.Div(style = {"padding":10}),# For vertical space
                html.H4("Corona Virus Canada Cases by Province",
                style=heading2, className = "container"),
                html.P("Hover over the provinces to view the trends for province-wise confirmed and death cases",
                    style = small_italics)
            ]),

            html.Div(style = {"padding":10}),# For vertical space
            html.Div([ # Div tag for Canada Bubble Map
                html.Div([
                    dcc.Graph(id='canada1',
                    config={'displayModeBar':False,
                            # 'staticPlot':True,
                            'responsive': True,
                            'doubleClick':False },
                    style = {"height":"50vh"},
                    hoverData={'points': [{'customdata': 'Alberta'}]}),
                ],style = graph_style,className="six columns"),
                html.Div([
                    dcc.Graph(id='canada2',
                    config={'displayModeBar':False,
                            # 'staticPlot':True,
                            'responsive': True,
                            'doubleClick':False },
                    style = {"height":"50vh"},
                    hoverData={'points': [{'customdata': 'Alberta'}]}),
                ],style = graph_style,className="six columns"),
            ],className="row"),
            html.Div(style = {"padding":10}),# For vertical space
            html.Div([ # Div tag for line and bar chart
                html.Div([
                        html.Div([
                            dcc.Graph(id='canada1-line',
                            config={'displayModeBar':False,
                                    # 'staticPlot':True,
                                    'responsive': True,
                                    'doubleClick':False },
                            style = {"height":"40vh"}),
                        ],className="three columns"),
                        html.Div([
                            dcc.Graph(id='canada1-bar',
                            config={'displayModeBar':False,
                                    # 'staticPlot':True,
                                    'responsive': True,
                                    'doubleClick':False },
                            style = {"height":"40vh"}),
                        ],className="three columns"),
                ]),
                html.Div([# Div tag for line and bar chart
                        html.Div([
                            dcc.Graph(id='canada2-line',
                            config={'displayModeBar':False,
                                    # 'staticPlot':True,
                                    'responsive': True,
                                    'doubleClick':False },
                            style = {"height":"40vh"}),
                        ],className="three columns"),
                        html.Div([
                            dcc.Graph(id='canada2-bar',
                            config={'displayModeBar':False,
                                    # 'staticPlot':True,
                                    'responsive': True,
                                    'doubleClick':False },
                            style = {"height":"40vh"}),
                        ],className="three columns"),
                    ]),
                ],style = graph_style),
            ]),
        ]),

        #<----------------------------- Tab 2---------------------------------->

        #<----------------------------- Tab 3---------------------------------->

        dcc.Tab(label='Analytics',
        value='tab-3',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div([ # Outer div tag for the page
                html.Div([ # start of first graph for tab 3
                    html.Div(style = {"padding":20}),# For vertical space
                        html.Div([
                            html.H2("Number of days since first case Vs current figures",
                            style=heading2, className = "container"),
                            html.P(" Comparison of cases between countries based on the number of days since first case",
                                style = div_small_text1 )
                        ], style= title_box,),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([# Div for dropdown
                        html.Div([
                            html.P("Select the data to view"),
                            dcc.Dropdown(
                                   id='tab-3-Dropdown1',
                                   options=target_options1,
                                   value='Confirmed',
                                   style={'width':'60%', 'text-align':'left',
                                   'color':colors["text1"],'float':'center'}
                               )], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                        html.Div([
                              html.P("Select the number of countries"),
                              dcc.Dropdown(
                                  id='tab-3-Dropdown2',
                                  options=top_options,
                                  value="Top 20",
                                  style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                              )], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                    ], style=title_box,className = "container"),

                    html.Div(style = {"padding":20}),# For vertical space
                    html.Div([# Div for First graph
                       dcc.Graph(
                                   id='no-of-days',
                                   config={'displayModeBar':False,
                                           # 'staticPlot':True,
                                           'responsive': True,
                                           'doubleClick':False },
                                   style = {"height":"80vh",'float':'center'}),
                        ],style=graph_style),

                    ]), # End of Div for first graph

            html.Div([ # Start of second graph of tab 3
                html.Div(style = {"padding":20}),# For vertical space
                    html.Div([
                        html.H2("Calendar Heatmap of New Cases",
                        style=heading2, className = "container"),
                        html.P("By World and Countries", style = div_small_text1)
                    ], style= title_box),
                html.Div(style = {"padding":10}),# For vertical space

                html.Div([ # Div for dropdown
                    html.Div([
                        html.P("Select Global/Country"),
                        dcc.Dropdown(
                               id='tab-3-Dropdown5',
                               options=country_options1,
                               value='Global',
                               style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                           ),
                    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                html.Div([# Div for dropdown

                          html.P("Select the data to view"),
                           dcc.Dropdown(
                                  id='tab-3-Dropdown6',
                                  options=target_options3,
                                  value="New Confirmed",
                                  style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                              ),
                     ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

                ],style = title_box, className = "container"),

                html.Div(style = {"padding":20}),# For vertical space

                html.Div([ # Div for heatmap
                       dcc.Graph(
                                   id='heatmap',
                                   config={'displayModeBar':False,
                                           # 'staticPlot':True,
                                           'responsive': True,
                                           'doubleClick':False },
                                   style = {"height":"100vh",'float':'center'}),
                ],style=graph_style),

                ]), # End of Div for second graph of tab 3
            html.Div([ # Start for third graph of tab 3
                html.Div(style = {"padding":20}),# For vertical space
                html.Div([
                    html.H2("Hierarchical contribution Of Cases",
                        style=heading2, className = "container"),
                    html.P("By Countries and Province/States", style = div_small_text1)
                ], style= title_box),
                html.Div(style = {"padding":10}),# For vertical space
                html.Div([ # Div for dropdowns
                    html.Div([# First dropdown
                        html.P("Select Global/Country"),
                        dcc.Dropdown(
                               id='tab-3-Dropdown3',
                               options=country_options,
                               value='Global',
                               style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                           ),
                    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                    html.Div([ # Second dropdown

                          html.P("Select the data to view"),
                           dcc.Dropdown(
                                  id='tab-3-Dropdown4',
                                  options=target_options,
                                  value="Confirmed",
                                  style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
                              ),
                      ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

                ],style = title_box, className = "container"),

                html.Div(style = {"padding":20}),# For vertical space

                html.Div([
                        # html.Div([ # Div for treemap and sunburst for tab 3
                        #    dcc.Graph(
                        #                id='treemap',
                        #                style = {"height":"70vh",'float':'center'}),
                        # ],className = "six columns"),

                        html.Div([
                           dcc.Graph(
                                       id='sunburst',
                                       config={'displayModeBar':False,
                                               # 'staticPlot':True,
                                               'responsive': True,
                                               'doubleClick':False },
                                       style = {"height":"80vh",'float':'center'}),
                        ],className = "twelve columns"),
                    ],style = graph_style),
                ]), # End of Div for third graph of tab 3
            ]),

        ]),

        #<---------------------- End of Tab 3---------------------------------->

        #<----------------------------- Tab 4---------------------------------->
        # Sart of Tab 4
        dcc.Tab(label='Weekly Forecast & Trends',
        value='tab-4',
        style=tab_style,
        selected_style=tab_selected_style,
        children = [
            html.Div([
                html.Div([ # Outer div tag for tab 4
                    html.Div(style = {"padding":20}),# For vertical space
                    html.Div([ # Div for title
                        html.H2("Current Trend and Forecast for a Week",
                            style=heading2, className = "container"),
                        html.P("Estimated values for the upcoming week using Auto Regression by SARIMAX algorithm",
                            style = div_small_text1)
                    ], style=title_box),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([ # div for dropdown
                        html.Div([
                            html.P("Select the data to view"),
                            dcc.Dropdown(
                                   id='tab-4-Dropdown1',
                                   options=target_options1,
                                   value='Confirmed',
                                   style={'width':'70%', 'text-align':'left', 'color':colors["text1"]}
                               ),
                        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
                        html.Div([# div for dropdown

                              html.P("Select the group of Countries"),
                               dcc.Dropdown(
                                      id='tab-4-Dropdown2',
                                      options=countries_options,
                                      value='Top 10',
                                      style={'width':'70%', 'text-align':'left', 'color':colors["text1"]}
                                  ),
                          ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
                    ], style=title_box,className = "container"),

                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([# div for forecast graph
                       dcc.Graph(
                                   id='forecast',
                                   config={'displayModeBar':False,
                                           # 'staticPlot':True,
                                           'responsive': True,
                                           'doubleClick':False },
                                   style = {"height":"80vh"},
                                   className = "twelve columns"),
                    ],style = chart_box1,className="row"),
                html.Div(style = {"padding":40}),# For vertical space

                html.Div([ # Start of second graph in tab 4
                    html.Div([
                        html.Div(style = {"padding":10}),# For vertical space
                        html.H2("Weekly Moving Average of New Cases Vs Total",
                            style=heading2, className = "container"),
                        html.P("Comparison of New cases with Total cases in linear and logarithmic scale",
                            style = div_small_text1),
                        html.P("Logarithmic scale gives an upward 45-degree trend, "+
                        "and a dip from that indicates downward trend from exponential trend on linear scale",
                            style = small_italics1)

                    ], style=title_box),
                    html.Div(style = {"padding":10}),# For vertical space
                    html.Div([# Div for dropdowns

                        html.Div([# Div for radio button
                              html.P("Select the Scale"),
                               dcc.RadioItems(
                                      id='tab-4-scale',
                                      options=scale_options,
                                      value='Linear',
                                      labelStyle={'display': 'inline-block'},
                                      style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
                                  ),
                          ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),
                        html.Div([ # Div for dropdown
                            html.P("Select the data to view"),
                            dcc.Dropdown(
                                   id='tab-4-Dropdown4',
                                   options=target_options1,
                                   value='Confirmed',
                                   style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
                               ),
                        ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),

                    ], style=title_box,className = "container"),

                        html.Div(style = {"padding":10}),# For vertical space
                        html.Div([
                           dcc.Graph(
                                       id='moving-average',
                                       config={'displayModeBar':False,
                                               # 'staticPlot':True,
                                               'responsive': True,
                                               'doubleClick':False },
                                       style = {"height":"80vh"},
                                       className = "twelve columns"),
                        ],style = chart_box1,className="row"),

                    ]), # End of Div for second graph moving average tab 4

                ]),
            ])

        ]),
        #<------------------------End of Tab 4---------------------------------->

        # #<----------------------------- Tab 5---------------------------------->
        # dcc.Tab(label='COVID Research Clustering ',
        # value='tab-5',
        # style=tab_style,
        # selected_style=tab_selected_style,
        # children = [
        #     html.Div([
        #         html.Div(style = {"padding":10}),# For vertical space
        #         html.Div([ # Title div
        #             html.H2("Visualization of Clustering Results",
        #             style=heading2, className = "container"),
        #             html.P("Dimension Reduction by T-SNE & Clustering by K-Means",
        #                 style = small_italics)
        #         ], style= title_box),
        #         html.Div(style = {"padding":10}),# For vertical space
        #         html.Div(style = {"padding":20}),# For vertical space
        #         html.Div([ # Div for dropdown
        #               html.P("Select the number of clusters"),
        #                dcc.Dropdown(
        #                       id='tab-5-option1',
        #                       options=single_level_options,
        #                       value='10 Clusters',
        #                       # labelStyle={'display': 'inline-block'},
        #                       style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
        #                   ),
        #           ], style=title_box, className = "container"),
        #
        #           html.Div([# Div for first row of graphs for tab 5
        #             html.Div([# Scatter plot
        #                 dcc.Graph(id='scatter_cluster',style = {"height":"80vh"}),
        #
        #             ],style = graph_style,className="six columns"),
        #
        #               html.Div([
        #                 html.Div([ # Div for bubble map
        #                     dcc.Graph(id='bubble_cluster',style = {"height":"80vh"}),
        #                 ],style = graph_style,className="six columns"),
        #             ],className="row"),
        #     ]), # End of second row of graphs for tab 5
        #         html.Div(style = {"padding":10}),# For vertical space
        #
        #     html.Div([ # Start of second row of graphs for tab 5
        #         html.Div(style = {"padding":10}),# For vertical space
        #         html.Div([
        #             html.H2("Hierarchical Relationship of Articles to Clusters",
        #             style=heading2, className = "container"),
        #             html.P("Dimension Reduction by T-SNE & Clustering by K-Means",
        #                 style = small_italics)
        #         ], style= title_box),
        #
        #
        #         html.Div(style = {"padding":20}),# For vertical space
        #             html.Div([ # Div for dropdowns
        #                 html.Div([ # Div for dropdown
        #                       html.P("Select the no. of clusters for Single-level clustering"),
        #                        dcc.Dropdown(
        #                               id='tab-5-option3',
        #                               options=multi_level_options,
        #                               value='5 Parents-5 Child Clusters',
        #                               style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
        #                           ),
        #                   ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        #
        #                 html.Div([ # Div for dropdown
        #                     html.P("Select the no. of clusters for Multi-level clustering"),
        #                             dcc.Dropdown(
        #                                    id='tab-5-option2',
        #                                    options=single_level_options,
        #                                    value='5 Clusters',
        #                          style={'width':'60%', 'text-align':'left', 'color':colors["text1"]}
        #                        ),
        #                 ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        #             ],style = title_box, className = "container"),
        #
        #         html.Div([# Div for sunburst graphs for tab 5
        #             html.Div([
        #                 dcc.Graph(id='sunburst1',style = {"height":"80vh"}),
        #             ],style = graph_style,className="six columns"),
        #             html.Div([
        #                 html.Div([
        #                     dcc.Graph(id='sunburst2',style = {"height":"80vh"}),
        #                 ],style = graph_style,className="six columns"),
        #             ],className="row"), # End of sunburst graphs
        #         ]),
        #         html.Div(style = {"padding":10}),# For vertical space
        #     ]), # End of second row of graphs for tab 5
        #
        #     html.Div([ # Start of third row of graphs for tab 5
        #         html.Div(style = {"padding":10}),# For vertical space
        #         html.Div([
        #             html.H2("Hierarchical Relationship of Articles to Clusters",
        #             style=heading2, className = "container"),
        #             html.P("Dimension Reduction by T-SNE & Clustering by K-Means",
        #                 style = small_italics)
        #         ], style= title_box),
        #         html.Div(style = {"padding":10}),# For vertical space
        #         html.Div([ # Div for dropdowns
        #               html.P("Select the no. of clusters for Multi-level clustering"),
        #                dcc.Dropdown(
        #                       id='tab-5-option4',
        #                       options=multi_level_options,
        #                       value='5 Parents-5 Child Clusters',
        #                       # labelStyle={'display': 'inline-block'},
        #                       style={'width':'80%', 'text-align':'left', 'color':colors["text1"]}
        #         )], style=title_box, className = "container"),
        #         html.Div([ # Div for dendrograms
        #             dcc.Graph(id='dendrogram1',
        #             style = {"height":"100vh"},
        #             className = "container"),
        #         ],className="twelve columns"),
        #         html.Div(style = {"padding":10}),# For vertical space
        #         ]), # End of third row of graph for tab 5
        #     ]), # End of outer div for tab 5
        # ])

        #<-----------------------End of Tab 5---------------------------------->
    ])
]) # End App layout



""" ###################################################
App Call Backs for TAB 1 - Global Trends
###################################################"""

@app.callback(
    Output('choropleth','figure'),
    [Input('option', 'value')])
def update_table(column):
        """
        Function to update the graph based on selected column
        Arguments:
            column: Type of case from the dropdown
        Returns:
            Updated Choropleth graph
        """

        # Condition for colorscale
        if column == 'Recovered':
            colorscale = "greens"
        elif column == 'Death':
            colorscale = colorscales["Death"]
        else:
            colorscale = colorscales["Confirmed"]

        # Preparing custom hover text
        my_text = [country+'<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+'<br>Deaths:'+'{:,d}'.format(deaths)+
      '<br>Recovered: '+'{:,d}'.format(recovered)+'<br>Fatality Rate:'+'{:.2f} %'.format(fatality)+
      '<br>Latest New Cases: '+'{:,d}'.format(new_cases) +"<extra></extra>"
      for country, confirmed, deaths, recovered, fatality, new_cases
        in zip(list(country_df['Country/Region']),list(country_df['Confirmed']), list(country_df['Death']),
        list(country_df['Recovered']), list(country_df['Fatality Rate']),
          list(country_df['New Confirmed']))]

        # Creating Choropleth graph
        fig = go.Figure(go.Choropleth(locationmode = 'country names', locations=country_df['Country/Region'], z=country_df[column],
                                            colorscale= colorscale,
                                            zmin=country_df[column].min(), zmax=country_df[column].max(),
                                            marker_opacity=1, marker_line_width=0.5,
                                            text = country_df['Country/Region'],
                                            customdata = country_df['Country/Region'],
                                            showscale = False,
                                                hovertemplate= my_text))
        # Updating layout
        fig["layout"].update(paper_bgcolor=colors["graph_map_color"], plot_bgcolor=colors["graph_map_color"])

        # fig.update_traces(showscale=False)
        # Adding the name of the continents on top of Choropleth as annotations
        annotations = []
        continents = ['North America', 'South America', 'Africa','Europe',  'Asia', 'Australia'," ", " "]
        Lat = [0.165,0.29,0.557,0.56,0.76,0.90,0,1]
        Long = [0.698,0.47,0.560,0.72,0.64,0.40,0,1]
        if column == 'Confirmed':
            color = "white"
        else:
            color = "black"
        # fig.add_trace(go.Scatter(
        #         x=Lat,
        #         y=Long,
        #         mode="markers+text",
        #         # name="Markers and Text",
        #         text=continents,
        #         textposition="top center",
        #          textfont=dict(
        #                 family="sans serif",
        #                 size=14,
        #                 color=color
        #             ),
        #         showlegend = False,
        #
        #
        #     ))
        #     fig.update_xaxes(showticklabels=False)
        #     fig.update_yaxes(showticklabels=False)


        for lat,long,continent in zip(Lat,Long,continents):
                annotations.append(dict(xref='paper', yref='paper', x=lat, y=long,
                                            text= continent,
                                            font=dict(size=12, color=color),
                                            showarrow=False))
        # # Adding annotations and others to layout
        fig.update_layout(
        annotations = annotations,
                            geo=dict(
                                showframe=False,
                                showcoastlines=False,
                                projection_type='equirectangular',
                                ),
                                dragmode= False,
                                margin={"r":0,"t":0,"l":0,"b":0},
                                template= template,
                        )
        return fig


@app.callback(
    Output('bubblemap','figure'),
    [Input('optionbubble', 'value')])
def update_table(column):
        """
        Function to update the graph based on selected column
        Arguments:
            column: Type of case from the dropdown
        Returns:
            Updated bubblemap graph
        """
        alldf = countryDays_df
        # Getting all dates in type datatime
        alldf['Date'] = pd.to_datetime(alldf['Date'])
        # Finding the number of weeks
        # weeknum = [int(i.strftime("%V")) for i in list(alldf['Date'])]
        alldf['Date'] = alldf['Date'].dt.strftime('%x')
        count_countries = (alldf['Country/Region']).count()
        # Creating Scatter geo bubblemap
        fig = px.scatter_geo(alldf,
                    lat = "Lat",
                    lon = "Long",
                    animation_frame='Date',animation_group = 'Country/Region',
                    size_max = 100,
                    hover_name = "Country/Region",
                    hover_data = ['Confirmed','Active','Death','Recovered','Fatality Rate','New Confirmed'],
                    size=alldf[column],
                    )

        # Adding continents on top of bubblemap as annotations
        # annotations = []
        # continents = ['North America', 'South America', 'Africa','Europe',  'Asia', 'Australia'," "," "]
        # Lat = [0.17,0.295,0.557,0.63,0.76,0.89,0,1]
        # Long = [0.76,0.45,0.560,0.82,0.69,0.38,0,1]
        # fig.add_trace(go.Scatter(
        #         x=Lat,
        #         y=Long,
        #         mode="markers+text",
        #         # name="Markers and Text",
        #         text=continents,
        #         textposition="top center",
        #          textfont=dict(
        #                 family="sans serif",
        #                 size=14,
        #                 color="Black"
        #             )
        #     ))

        # for lat,long,continent in zip(Lat,Long,continents):
        #         annotations.append(dict(xref='paper', yref='paper', x=lat, y=long,
        #                                     text= continent,
        #                                     font=dict(size=12, color=colors['text1']),
        #                                     showarrow=False))
        # Adding annotations and other conditions to the layout
        fig.update_layout(
                        # annotations = annotations,
                            geo=dict(
                                showframe=False,
                                showcoastlines=True,
                                projection_type='equirectangular'),
                            dragmode = False,
                            showlegend=False,
                            # dragmode= False,
                            template = "plotly",
                            margin={"r":0,"t":0,"l":0,"b":0},
                            paper_bgcolor=colors["graph_bg_color"], plot_bgcolor=colors["graph_bg_color"]
                        )

        return fig

@app.callback(Output('type','children'),
            [Input('choropleth','clickData')])
def update_div(clickData):
    """
    Function to update the title on the top-right panel Global/Country name
    based on Click Data from Choropleth
    Arguments:
        clickData: Click data of country selected from Choropleth
    Returns:
        Updated title for top right panel
    """
    country = clickData['points'][0]['customdata']
    # Excluding Syria and France as there were duplicates
    if country == "Syria" or country == "France":
        country = ""
    return_divs = []
    provincedf = latest_df1.loc[latest_df1['Country/Region'] == country]
    provinces = provincedf["Location"]
    if country == "" :
            return_divs.append(html.P('World',style={'text-align':'center','font-family':'sans-serif', 'color': '#303030', 'font-size': '15px'}))
    else: # Appending the value for Country name
        return_divs.append(html.P(country,style={'text-align':'center','font-family':'sans-serif', 'color': '#303030', 'font-size': '15px'}))
    return return_divs


@app.callback(Output('top-7','children'),
            [Input('optionbubble','value')])
def update_div(case):
    """
    Function to update the bottom left panel based on selected case from dropdown
    Arguments:
        column: Type of case from the dropdown
    Returns:
        Updated values of the div for bottom left panel
    """
    return_divs=[]
    # Choosing the dataframe to be used according to each case
    if(case == "Confirmed"):
        for i in range(10):
            top = top_conf_df.iloc[i]
            # print(top)
            return_divs.append(
                html.Div(children = [html.P(top["Country/Region"] ,
                        className = "top-count-name",
                        style = {'font-size': '14px','font-style':'bold'}),
                        html.P(''+'{:,}'.format(top[case].astype(int)),
                        style={'text-align':'center','font-family':'sans-serif',
                        'color': colors[case], 'font-size': '20px'})],
                        className = "topcount"))
    if(case == "Active"): # Choosing Dataframe for Active cases
        for i in range(10):
            top = top_active_df.iloc[i]
            return_divs.append(
                html.Div(children = [html.P(top["Country/Region"] ,
                          className = "top-count-name",
                          style = {'font-size': '14px'}),
                          html.P(''+'{:,}'.format(top[case].astype(int)),
                          style={'text-align':'center','font-family':'sans-serif',
                          'color': colors[case], 'font-size': '20px'})],
                          className = "topcount"))
    if(case == "Death"): # Choosing DataFrame for Death cases
        for i in range(10):
            top = top_death_df.iloc[i]
            return_divs.append(
                html.Div(
                          children = [html.P(top["Country/Region"] ,
                          className = "top-count-name",
                          style = {'font-size': '14px'}),
                          html.P(''+'{:,}'.format(top[case].astype(int)),
                          style={'text-align':'center',
                          'font-family':'sans-serif', 'color': colors[case], 'font-size': '20px'})],
                          className = "topcount"))
    if(case == "Recovered"): # Choosing DataFrame for Recovered cases
        for i in range(10):
            top = top_recovered_df.iloc[i]
            return_divs.append(
                html.Div(children = [html.P(top["Country/Region"] ,
                        className = "top-count-name",
                        style = {'font-size': '14px'}),
                        html.P(''+'{:,}'.format(top[case].astype(int)),
                        style={'text-align':'center','font-family':'sans-serif',
                        'color': colors[case], 'font-size': '20px'})],
                        className = "topcount"))
    return return_divs


@app.callback(Output('div-1','children'),
            [Input('choropleth','clickData')])
def update_div(clickData):
    """
    Function to update the first column of country/province names on the top-right Panel
    based on the click data from Choropleth
    Arguments:
        clickData: Click data containing country selected from Choropleth
    Returns:
        Updated Div with first column values for top right panel
    """

    country = clickData['points'][0]['customdata']

    # Excluding Syria and France became of duplicate values
    if country == "Syria" or country == "France":
        country = ""
    return_divs = []
    provincedf = latest_df1.loc[latest_df1['Country/Region'] == country]
    provinces = list(provincedf["Location"])
    if country == 'Canada':
        if 'Recovery aggregated' in provinces:
            provinces.remove("Recovery aggregated")

    return_divs.append(html.Div(
                    children = [html.P('Country or',
                    style={'text-align':'center','font-family':'sans-serif',
                    'width' : '10vh', 'font-size': '12px', 'color': '#303030'}),
                    html.P("Province ",
                    style={'text-align':'center','font-family':'sans-serif',
                    'width' : '10vh', 'font-size': '12px', 'color': '#303030'})]))
    if country == "":
        for country in countries:
            return_divs.append(html.Div(html.P(""+country.upper(), style = div_small_text)))
    else:
        for province in provinces:
            return_divs.append(html.Div(html.P(""+province.upper(), style = div_small_text)))
    return return_divs

@app.callback(Output('div-2','children'),
            [Input('choropleth','clickData')])
def update_div(clickData):
    """
    Function to update the second column of confirmed cases on the top-right Panel
    based on the click data from Choropleth
    Arguments:
        clickData: Click data containing country selected from Choropleth
    Returns:
        Updated Div with second column values for top right panel
    """
    country = clickData['points'][0]['customdata']
    # Excluding Syria and Frane because of duplicate values
    if country == "Syria" or country == "France":
        country = ""
    return_divs = []
    provincedf = latest_df1.loc[latest_df1['Country/Region'] == country]
    provinces = provincedf["Location"]
    if country == "":
        return_divs.append(html.Div(
                        children = [html.P('Confirmed',
                        style={'text-align':'center','font-family':'sans-serif',
                        'width' : '10vh', 'font-size': '12px', 'color': '#303030'}),
                        html.P(""+ confirmedVal,
                        style = {'font-size': '14px', 'font-style':'bold',
                        'font-style':'bold' ,'text-align':'center', 'color': colors['Confirmed']})]))
        for country in countries:
            confirmed = desc_country_df.loc[desc_country_df['Country/Region'] == country, 'Confirmed'].iloc[0]
            return_divs.append(html.Div(html.P(""+"{:,d}".format(confirmed), style = div_small_text)))
    else:
        confirmed = (desc_country_df.loc[desc_country_df['Country/Region'] == country, "Confirmed"].iloc[0])

        return_divs.append(html.Div(
                        children = [html.P('Confirmed',
                        style={'text-align':'center','font-family':'sans-serif',
                        'width' : '10vh', 'font-size': '12px', 'color': '#303030'}),
                        html.P(""+'{:,d}'.format(confirmed),
                        style = {'font-size': '14px', 'font-style':'bold',
                        'text-align':'center', 'color': colors['Confirmed']})]))
        for province in provinces:
            confirmed = latest_df1.loc[latest_df1['Location'] == province, 'Confirmed'].iloc[0]
            return_divs.append(html.Div(html.P(""+"{:,d}".format(confirmed), style = div_small_text)))
    return return_divs


@app.callback(Output('div-3','children'),
            [Input('choropleth','clickData')])
def update_div(clickData):
    """
    Function to update the third column of death cases on the top-right Panel
    based on the click data from Choropleth
    Arguments:
        clickData: Click data containing country selected from Choropleth
    Returns:
        Updated Div with third column values for top right panel
    """
    country = clickData['points'][0]['customdata']
    # Excluding Syria and France
    if country == "Syria" or country == "France":
        country = ""
    return_divs = []
    provincedf = latest_df1.loc[latest_df1['Country/Region'] == country]
    provinces = provincedf["Location"]
    if country == "":
        return_divs.append(html.Div(
                        children = [html.P('Death',
                        style={'text-align':'center','font-family':'sans-serif',
                        'width' : '10vh', 'font-size': '12px', 'color': '#303030'}),
                        html.P(""+ DeathVal,
                        style = {'font-size': '14px', 'font-style':'bold',
                        'font-style':'bold' ,'text-align':'center', 'color': colors['Death']})]))
        for country in countries:
            death = desc_country_df.loc[desc_country_df['Country/Region'] == country, 'Death'].iloc[0]
            return_divs.append(html.Div(html.P(""+"{:,d}".format(death), style = div_small_text)))
    else:
        death = (desc_country_df.loc[desc_country_df['Country/Region'] == country, "Death"].iloc[0])
        return_divs.append(html.Div(
                        children = [html.P('Death',
                        style={'text-align':'center','font-family':'sans-serif',
                        'width' : '10vh', 'font-size': '12px', 'color': '#303030'}),
                        html.P(""+'{:,d}'.format(death),
                        style = {'font-size': '14px', 'font-style':'bold',
                        'text-align':'center', 'color': colors['Death']})]))
        for province in provinces:
            death = latest_df1.loc[latest_df1['Location'] == province, 'Death'].iloc[0]
            return_divs.append(html.Div(html.P(""+"{:,d}".format(death), style = div_small_text)))
    return return_divs


@app.callback(Output('div-4','children'),
            [Input('choropleth','clickData')])
def update_div(clickData):
    """
    Function to update the fourth column of Recovered cases on the top-right Panel
    based on the click data from Choropleth
    Arguments:
        clickData: Click data containing country selected from Choropleth
    Returns:
        Updated Div with fourth column values for top right panel
    """
    country = clickData['points'][0]['customdata']
    # Excluding Syria and France because of duplicate values
    if country == "Syria" or country == "France":
        country = ""
    return_divs = []
    provincedf = latest_df1.loc[latest_df1['Country/Region'] == country]
    provinces = provincedf["Province/State"]
    if country == "":
        return_divs.append(html.Div(
                children = [html.P('Recovered',
                style={'text-align':'center','font-family':'sans-serif',
                'width' : '10vh', 'font-size': '12px', 'color': '#303030'}),
                html.P(""+ RecoveredVal,
                style = {'font-size': '14px', 'font-style':'bold',
                'text-align':'center', 'color': colors['Recovered']})]))
        for country in countries:
            recovered = desc_country_df.loc[desc_country_df['Country/Region'] == country, 'Recovered'].iloc[0]
            return_divs.append(html.Div(html.P(""+"{:,d}".format(recovered), style = div_small_text)))

    else:
        recovered = desc_country_df.loc[desc_country_df['Country/Region'] == country, 'Recovered'].iloc[0]
        return_divs.append(html.Div(
                    children = [html.P('Recovered',
                    style={'text-align':'center','font-family':'sans-serif',
                    'width' : '10vh', 'font-size': '12px', 'color': '#303030'}),
                    html.P(""+ "{:,d}".format(recovered),
                    style = {'font-size': '14px', 'font-style':'bold',
                    'text-align':'center', 'color':colors['Recovered']})]))
        for province in provinces:
            # Adjusting the values of countries with province information for other
            # Cases but only country values for recovered cases
            if (latest_df1.loc[latest_df1['Country/Region']==country,'Recovered'].count()>2 and country != 'Canada'):
                recovered = latest_df1.loc[latest_df1['Location'] == province, 'Recovered'].iloc[0]
                return_divs.append(html.Div(html.P(""+"{:,d}".format(recovered), style = div_small_text)))
            else:
            # Condition for countries with recovered values available for provinces
                recovered = desc_country_df.loc[desc_country_df['Country/Region'] == country, 'Recovered'].iloc[0]
                return_divs.append(html.Div(html.P(""+"{:,d}".format(recovered), style = div_small_text)))
                return return_divs
    return return_divs

@app.callback(Output('onebar','figure'),
            [Input('option', 'value'),
             Input('choropleth','clickData')])
def update_figure(value, clickData):
    """
    Function to update the bar chart for new cases on the top right panel
    based on the click data from Choropleth and dropdown value
    Arguments:
        clickData: Click data containing country selected from Choropleth
        value: Dropdown value to select the column of the case
    Returns:
        Updated bar chart object for top right panel
    """

    # Setting up conditional colorscale
    if value == 'Recovered':
        colorscale = "greens"
    elif value == 'Death':
        colorscale = colorscales["Death"]
    else:
        colorscale = colorscales["Confirmed"]
    country = clickData['points'][0]['customdata']
    column = "New"+" "+value

    if country == "": # Global values
        fig = go.Figure(go.Bar(x=sumdf['Date'], y=sumdf[column],name=value,
                marker=dict(
                color = sumdf[column],
                colorscale = colorscale,)))
        country = "World"
    else: # Country specific values
        newcases_df = countryDays_df.loc[countryDays_df['Country/Region'] == country]
        newcases_df = newcases_df.sort_values(column,ascending = True)
        # Removing the entries of dates before the first confirmed case of that country
        limit = (newcases_df[column].values != 0).argmax()
        newcases_df = newcases_df[limit:]
        newcases_df = newcases_df.sort_values('Date',ascending = True)
        fig = go.Figure(go.Bar(x=newcases_df['Date'], y=newcases_df[column],
            marker=dict(color = newcases_df[column],colorscale = colorscale,), name=column))
    fig.update_layout( # Updating the layout
    title={
        'text': country+ " : " + column +" Cases",
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    font=dict(
        family="sans-serif",
        size=11.5,
        color= '#303030'
    ),
    dragmode = False,
    paper_bgcolor= colors['div_color1'],
    plot_bgcolor= colors['div_color1'],
    margin={"r":1,"t":45,"l":1,"b":0})
    return fig

@app.callback(Output('oneline','figure'),
            [Input('optionbubble', 'value')])
def update_figure(value):
    """
    Function to update the line chart for cumulative cases on the bottom right panel
    based on the dropdown value
    Arguments:
        value: Dropdown value to select the column of the case
    Returns:
        Updated line chart object for bottom right panel
    """
    limit = 10

    # selecting the source dataframe
    if(value == "Confirmed"):
        data = top_conf_df
    if(value == "Active"):
        data = top_active_df
    if(value == "Death"):
        data = top_death_df
    if(value == "Recovered"):
        data = top_recovered_df
    # Selecting top 10 countries
    top_countries = []
    top_countries = list(data[:limit]['Country/Region'])
    g_data = []
    fig = go.Figure()
    for country in top_countries:
        ndf = countryDays_df.loc[countryDays_df['Country/Region'] == country]
        fig.add_trace(go.Scatter( x=ndf['Date'],
                            y=ndf[value],
                            mode='lines',
                            name=country))
        fig.update_layout(dragmode = False)

    fig.update_layout(dragmode = False,
                    xaxis = dict(title='Date'),
                    yaxis = dict(title ='Number of '+value+' Cases'),
                    hovermode = 'closest'),

    fig.update_layout(
        title={
            'text': "Top 10 Countries: "+value,
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="sans-serif",
            size=11.5,
            color= '#303030'
        ),
        dragmode = False,
        paper_bgcolor= colors['div_color1'],
        plot_bgcolor= colors['div_color1'],
        margin={"r":1,"t":45,"l":1,"b":0})
    return fig

@app.callback(Output('doughnut','figure'),
            [Input('optionbubble', 'value')])
def update_figure(value):
    """
    Function to update the doughnut chart for cumulative cases on the bottom right panel
    based on the dropdown value
    Arguments:
        value: Dropdown value to select the column of the case
    Returns:
        Updated doughnut chart object for bottom right panel
    """
    # Selecting the dataframe to use
    limit = 10
    if(value == "Confirmed"):
        data = top_conf_df
    elif(value == "Active"):
        data = top_active_df
    elif(value == "Death"):
        data = top_death_df
    elif(value == "Recovered"):
        data = top_recovered_df
    labels = []

    # Getting the values for top 10 countries
    labels = list(data[:limit]['Country/Region'])
    values = list(data[:limit][value])
    # Adding doughnut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values= values, hole=.3,textinfo='label+percent',
                        marker=dict(colors=values, line=dict(color=[colors['text2']]*limit, width=0.5)))])
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    fig.update_layout(
        title={
            'text': "Top 10 Countries: "+value,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="sans-serif",
            size=11.5,
            color= '#303030'
        ),
        dragmode = False,
        showlegend=False,
        paper_bgcolor= colors['div_color1'],
        plot_bgcolor= colors['div_color1'],
        margin={"r":1,"t":45,"l":1,"b":0})
    return fig

""" ###################################################
App Call Backs for TAB 2 - Canada Trends
###################################################"""

def canada_map(column,n):
    """
    Function to create the bubble map for Canada
    Arguments:
        value: Case to be highlighted using the bubble map
    Returns:
        Updated bubble map object for Canada
    """
    fig = go.Figure()
    selected_df = canada_df[~canada_df['Location'].isin(['Canada','Diamond Princess','Grand Princess','Recovery aggregated'])]
    # Defining hover text
    my_text = [location+'<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+'<br>Deaths:'+'{:,d}'.format(deaths)+
  '<br>Fatality Rate:'+'{:.2f} %'.format(fatality)+
  '<br>Latest New Cases: '+'{:,d}'.format(new_cases)+'<br>Cases per 100,000 :'+'{:,d}'.format(ratio)
  for location, confirmed, deaths, fatality, new_cases, ratio
    in zip(list(selected_df['Location']),list(selected_df['Confirmed']), list(selected_df['Death']),
    list(selected_df['Fatality Rate']),
      list(selected_df['New Confirmed']), list(selected_df['Cases Per Population'])) ]

    # Adding Canada map
    trace1 = {"uid": "1a57419c-8c71-11e8-b0f0-089e0178c4cf",
    "mode": "markers+text", "name": "",
    "type": "scattergeo",
    "lat": list(selected_df['Lat']),
    "lon": list(selected_df['Long']),
      "marker": {
        "line": {"width": 1},
        "size": list(selected_df[column]/n),
        "color": list(selected_df[column]/n),
         },
      'customdata': selected_df['Location'],
      'text':  selected_df['Location'],
      'hovertemplate' :my_text,
      "textfont": {
        "size":10,
        },
      "textposition": ["top center", "middle left", "top center", "bottom center", "top right", "middle left", "bottom right", "bottom left", "top right", "top right"]
    }

    data = Data([trace1])
    layout = {
          "geo": {
            "scope": "north america",
            "lataxis": {"range": [40, 70]},
            "lonaxis": {"range": [-140, -30]}
          },
          'clickmode': 'event+select',
          'dragmode': False,
          'template' : "plotly",
          'margin': dict(l=30, r=10, b= 10),
          "title": "Canada: "+column + " Cases",
          'title_x':0.5,
          'title_y':0.96    ,
          'titlefont': dict(
              color=colors['text1'],
              size=22)
    }
    fig = Figure(data=data, layout=layout)
    return fig

@app.callback(Output('canada1','figure'),
        [Input('tab-3-Dropdown1','value')])
def update_figure(value):
    """
    Function to create the bubble map for Canada highlighting Confirmed cases
    Arguments:
        value: Dummy dropdown value for callback to work
    Returns:
        Updated bubble map object for Canada
    """
    fig = canada_map("Confirmed",300)
    return fig

@app.callback(Output('canada2','figure'),
        [Input('tab-3-Dropdown1','value')])
def update_figure(val):
    """
    Function to create the bubble map for Canada highlighting Death cases
    Arguments:
        value: Dummy dropdown value for callback to work
    Returns:
        Updated bubble map object for Canada
    """
    fig = canada_map("Death",25)
    return fig


@app.callback(Output('canada1-line','figure'),
        [Input('canada1','hoverData')])
def update_figure(hoverData):
    """
    Function to create the line chart for Canada for Cumulative Confirmed cases
    Arguments:
        hoverData: hoverdata passing the province name to line chart
    Returns:
        Updated line chart object for the selected province
    """
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]
    # Removing the initial date values without values
    province_df = province_df.sort_values('Date',ascending = True)
    limit = (province_df['Confirmed'].values != 0).argmax()
    province_df = province_df[limit:]

    fig = go.Figure(go.Scatter(x=province_df['Date'], y=province_df['Confirmed'],
                    mode='lines+markers',marker_color='orange',
                    name=province))
    fig.update_layout(
    title= province + " Total Confirmed: " + '{:,d}'.format(province_df['Confirmed'].max()) ,
    title_x= 0.5,
    titlefont= dict(
        color=colors['text1'],
        size=18
    ),
    dragmode = False,
    template = template,
    margin=dict(l=20, r=20),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    return fig

@app.callback(Output('canada1-bar','figure'),
        [Input('canada1','hoverData')])
def update_figure(hoverData):
    """
    Function to create the bar chart for Canada for new Confirmed cases
    Arguments:
        hoverData: hoverdata passing the province name to line chart
    Returns:
        Updated bar chart object for the selected province
    """
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]
    # Removing the initial date values without values
    province_df = province_df.sort_values('Date',ascending = True)
    limit = (province_df['New Confirmed'].values != 0).argmax()
    province_df = province_df[limit:]

    fig = go.Figure(go.Bar(x=province_df['Date'], y=province_df['New Confirmed'],
                        name=province, marker_color='orange'))

    latest_date = latest_df['Date'].max()
    fig.update_layout(
    title= province + " New Confirmed: "+ '{:,d}'.format(province_df.loc[province_df['Date'] == latest_date,'New Confirmed'].iloc[0]),
    title_x= 0.5,
    titlefont= dict(
        color=colors['text1'],
        size=18
    ),
    dragmode = False,
    margin=dict(l=20, r=20),
    template = template,
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    return fig

@app.callback(Output('canada2-line','figure'),
        [Input('canada2','hoverData')])
def update_figure(hoverData):
    """
    Function to create the line chart for Canada for Cumulative Death cases
    Arguments:
        hoverData: hoverdata passing the province name to line chart
    Returns:
        Updated line chart object for the selected province
    """
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]
    # Removing the initial date values without values
    province_df = province_df.sort_values('Date',ascending = True)
    limit = (province_df['Death'].values != 0).argmax()
    province_df = province_df[limit:]

    fig = go.Figure(go.Scatter(x=province_df['Date'], y=province_df['Death'],
                    mode='lines+markers',
                    name=province,marker_color='crimson'))
    fig.update_layout(
    title= province + " Total Deaths:" + '{:,d}'.format(province_df['Death'].max()),
    title_x= 0.5,
    titlefont= dict(
        color=colors['text1'],
        size=18
    ),
    dragmode = False,
    margin=dict(l=20, r=20),
    template = template,
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    return fig

@app.callback(Output('canada2-bar','figure'),
        [Input('canada2','hoverData')])
def update_figure(hoverData):
    """
    Function to create the bar chart for Canada for new Death cases
    Arguments:
        hoverData: hoverdata passing the province name to line chart
    Returns:
        Updated bar chart object for the selected province
    """
    province = hoverData['points'][0]['customdata']
    province_df = df.loc[df['Location'] == province]

    # Removing the initial date values without values
    province_df = province_df.sort_values('Date',ascending = True)
    limit = (province_df['New Death'].values != 0).argmax()
    province_df = province_df[limit:]
    fig = go.Figure(go.Bar(x=province_df['Date'], y=province_df['New Death'],
                            name=province, marker_color='crimson'))
    latest_date = latest_df['Date'].max()
    fig.update_layout(
    title= province + " New Deaths: "+ '{:,d}'.format(province_df.loc[province_df['Date'] == latest_date,'New Death'].iloc[0]),
    title_x= 0.5,
    titlefont= dict(
        color=colors['text1'],
        size=18
    ),
    dragmode = False,
    template = template,
    margin=dict(l=20, r=20),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)
    return fig

""" ###################################################
App Call Backs for TAB 3 - Analytics
###################################################"""

@app.callback(Output('no-of-days','figure'),
        [Input('tab-3-Dropdown1','value'),
        Input('tab-3-Dropdown2','value')])
def update_figure(y_axis,top):
    """
    Function to create the subplots of horizontal bar chart and line chart
    for number of days since the first case Vs current cumulative value for the case
    Arguments:
        y_axis: Dropdown value for the selected cases
        top: Dropdown value for the number of countries to be viewed
    Returns:
        Updated subplot object for the selected dropdown values
    """

    # Selecting the number of countries to view
    if top == "Top 20":
        top_num = 20
    elif top == "Top 30":
        top_num = 30
    elif top == "Top 40":
        top_num = 40

    # Setting the colorscale based on drop down values
    if y_axis == 'Recovered':
        line_color = "#21D12B"
        colorscale = colorscales["Recovered"]
    elif y_axis == 'Death':
        line_color = "red"
        colorscale = colorscales["Death"]
    else:
        line_color = "orange"
        colorscale = colorscales["Confirmed"]
    # Copying the rows with rows ! = 0
    grouped_df = df.loc[df[y_axis] != 0].copy()
    grouped_df = grouped_df.sort_values(['Date'], ascending = True)

    # Performing group by operation to aggregate the total number of days of the selected
    # Case from the dropdown values
    aggregations = {'Date':'first','Confirmed':'count','Active':'count','Death':'count','Recovered':'count'}
    count_df = grouped_df.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values
    count_df['NoOfDays'] = ((pd.to_datetime("now") - count_df['Date'])/np.timedelta64(1,'D')).astype(int)

    # Performin group by operation to aggregate current values of selected case
    aggregations = {'Date':'first','Confirmed':'sum','Active':'sum','Death':'sum','Recovered':'sum',
    'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}
    current_df = latest_df.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values

    count_df=count_df.sort_values(['NoOfDays'],ascending = True)
    current_df = current_df.set_index('Country/Region')
    current_df = current_df.reindex(index=count_df['Country/Region'])
    current_df = current_df.reset_index()

    # print(current_df.head())
    limit = len(current_df.index)-top_num

    # Preparing custom hover text
    my_text = [country+'<br>No. of days since: '+'{:,d}'.format(noofdays)+
    '<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+'<br>Deaths:'+'{:,d}'.format(deaths)+
  '<br>Recovered: '+'{:,d}'.format(recovered)+
  '<br>Latest New Cases: '+'{:,d}'.format(new_cases) +"<extra></extra>"
  for country,noofdays, confirmed, deaths, recovered, new_cases
    in zip(list(count_df['Country/Region'].iloc[limit:]),list(count_df['NoOfDays'].iloc[limit:]),
    list(current_df['Confirmed'].iloc[limit:]), list(current_df['Death'].iloc[limit:]),
    list(current_df['Recovered'].iloc[limit:]), list(current_df['New Confirmed'].iloc[limit:]))]

    # Initializing subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001,)
    # Adding horizontal bar chart
    fig.append_trace(go.Bar(x=count_df['NoOfDays'].iloc[limit:],
                    y=count_df['Country/Region'].iloc[limit:],
                    marker=dict(
                        color=count_df['NoOfDays'].iloc[limit:],
                        colorscale = colorscale,
                        line=dict(
                            # color='rgba(50, 171, 96, 1.0)',
                            width=1),
                    ),
                    # hovername = count_df['Country/Region'],
                    hovertemplate = my_text,
                    name='No. of days since',
                    orientation='h',
                ), 1, 1)
    # Adding line chart
    fig.append_trace(go.Scatter(
        x=current_df[y_axis].iloc[limit:], y=current_df['Country/Region'].iloc[limit:],
        mode='lines+markers',
        line_color= line_color,
        line_width = 5,
        name='Total '+y_axis+' Cases',
        # hover_data =
        hovertemplate = my_text,
        textposition="middle right",
    ), 1, 2)

    fig.update_layout(
    dragmode = False,
    yaxis=dict(
        showgrid=False, showline=True, showticklabels=True, domain=[0, 0.85], ),
    yaxis2=dict(
        showgrid=False, showline=True, showticklabels=False, linecolor='rgba(102, 102, 102, 0.8)',
        linewidth=2, domain=[0, 0.85],
    ),
    xaxis=dict(
        zeroline=False, showline=False, showticklabels=True, showgrid=True, domain=[0, 0.42],),
    xaxis2=dict(
        zeroline=False, showline=True, showticklabels=False, showgrid=False, domain=[0.47, 1],
         side='top', dtick=25000,visible = False,
    ),
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],)

    annotations = []
    # Adding labels to the charts
    for ydn, yd, xd in zip(current_df[y_axis].iloc[limit:], count_df['NoOfDays'].iloc[limit:], count_df['Country/Region'].iloc[limit:]):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2', y=xd, x=ydn+5*current_df[y_axis].mean(),
                                text=xd+": "+'{:,}'.format(ydn) ,
                                font=dict(family='Arial', size=12, color=colors['graph_text']),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1', y=xd, x=yd+3,
                                text=str(yd) ,
                                font=dict(family='Arial', size=12, color=colors['graph_text']),
                                showarrow=False))
        annotations.append(dict(xref='paper', yref='paper', x=0.3, y=0.98,
                                text='No. of days since first case Vs '+'Total ('+y_axis+' cases)',
                                font=dict(size=20, color=colors['text1']),
                                showarrow=False))
        # labeling the bar net worth
        # annotations.append(dict(xref='paper', yref='paper', x = 0.85, y = 0.98,
        #                         text='Total '+y_axis ,
        #                         font=dict(size=20, color=colors['text1']),
        #                         showarrow=False))


    fig.update_layout(annotations=annotations,
    title_x= 0.5,
    dragmode = False,
    template = template,
    titlefont= dict(
        color=colors['heading'],
        size=22
    ),
    margin=dict(l=20, r=20, t=20, b=0))
    return fig

# @app.callback(Output('treemap','figure'),
#         [Input('tab-3-Dropdown3','value'),
#         Input('tab-3-Dropdown4','value')])
# def update_figure(option,y_axis):
#     """
#     Function to create treemap to show hierarchical contribution of countries
#     or provinces for the selected case from dropdown
#     Arguments:
#         y_axis: Dropdown value for the selected case
#         option: Dropdown value for the selected country/Global
#     Returns:
#         Updated treemap object for the selected dropdown values
#     """
#     # setting the colorscales based on cases
#     if y_axis == 'Recovered':
#         colorscale = colorscales["Recovered"]
#     elif y_axis == 'Death':
#         colorscale = colorscales["Death"]
#     elif y_axis == "Active":
#         colorscale = colorscales["Active"]
#     else:
#         colorscale = colorscales["Confirmed"]
#
#     # Selecting the dataframe according to the option dropdown value
#     if option == 'Global':
#         selected_df = country_df
#         pathlist = ['Country/Region']
#         data = ['Country/Region', 'Confirmed','Death','Recovered','New Confirmed']
#     else:
#         selected_df = latest_df.loc[latest_df['Country/Region']==option]
#         pathlist = ['Location']
#         data = ['Country/Region','Province/State', 'Confirmed','Death','Recovered','New Confirmed']
#     selected_df = selected_df[selected_df[y_axis]>0]
#
#     # Creating sunburst
#     fig = px.treemap(selected_df, path=pathlist, values=y_axis,template = template,
#                           color=y_axis, color_continuous_scale=colorscale,
#                           color_continuous_midpoint=np.average(selected_df[y_axis], weights=selected_df[y_axis]))
#
#     fig.update_layout(
#         template=template,
#         margin=dict(l=20, r=10, t=10, b=10))
#     return fig

@app.callback(Output('sunburst','figure'),
        [Input('tab-3-Dropdown3','value'),
        Input('tab-3-Dropdown4','value')])
def update_figure(option,y_axis):
    """
    Function to create sunburst to show hierarchical contribution of countries
    or provinces for the selected case from dropdown
    Arguments:
        y_axis: Dropdown value for the selected case
        option: Dropdown value for the selected country/Global
    Returns:
        Updated sunburst object for the selected dropdown values
    """

    # Setting the colorscale based on the case type
    if y_axis == 'Recovered':
        colorscale = colorscales["Recovered"]
    elif y_axis == 'Death':
        colorscale = colorscales["Death"]
    elif y_axis == "Active":
        colorscale = colorscales["Active"]
    else:
        colorscale = colorscales["Confirmed"]
    # Selecting the dataframe based on the dropdown option value
    if option == 'Global':
        selected_df = latest_df
        pathlist = ['Country/Region','Location']

    else:
        selected_df = latest_df.loc[latest_df['Country/Region']==option]
        pathlist = ['Location']

    selected_df = selected_df[selected_df[y_axis]>0]

    # Creating the sunburst
    fig = px.sunburst(selected_df, path=pathlist,
                    values= y_axis, color=y_axis, color_continuous_scale=colorscale,
                  color_continuous_midpoint=np.average(selected_df[y_axis], weights=selected_df[y_axis]))

    fig.update_layout(
        template=template,
        dragmode = False,
        margin=dict(l=10, r=10, t=10, b=10, autoexpand = True),
        uniformtext_minsize=12, uniformtext_mode='hide')
    return fig

@app.callback(Output('heatmap','figure'),
        [Input('tab-3-Dropdown5','value'),
        Input('tab-3-Dropdown6','value')])
def update_figure(option,y_axis):
    """
    Function to create heatmap to show hierarchical contribution of countries
    or provinces for the selected case from dropdown
    Arguments:
        y_axis: Dropdown value for the selected case
        option: Dropdown value for the selected country/Global
    Returns:
        Updated heatmap object for the selected dropdown values
    """
    aggregations = { 'Confirmed':'sum','Active':'sum','Death':'sum','Recovered':'sum','Fatality Rate':'mean',
            'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}

    # Selecting the dataframe based on the option dropdown value
    if option == 'Global':
        selected_df=df.groupby(["Date"],as_index=False).agg(aggregations) #groupby Country and Date values
    else:
        selected_df = countryDays_df.loc[countryDays_df['Country/Region']==option]
    # print(selected_df.dtypes)
    selected_df[y_axis] = pd.to_numeric(selected_df[y_axis], errors='coerce',downcast='integer')
    selected_df['Date'] = pd.to_datetime(selected_df['Date']) #Converting to datetype
    selected_df = selected_df.sort_values(['Date'], ascending = True )

    # finding the date range in the selected dataframe
    d1 = selected_df['Date'].min()
    d2 = selected_df['Date'].max()
    delta = d2 - d1

    # Finding all the days in the delta date range
    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days+1)] #gives a list with datetimes for each day a year

    # Finding the number of weekdays from the dates
    weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,...] (ticktext in xaxis dict translates this to weekdays
    # Finding the week number from the dates
    weeknumber_of_dates = [int(i.strftime("%V")) for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,...] name is self-explanatory
    # Finding the month name from the dates
    months = [(i.strftime("%b")) for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,...] name is self-explanatory
    z = list(selected_df[y_axis]) # z-axis value

    # Setting the colorscale based on the case type
    if y_axis == 'New Recovered':
        line_color = "white"
        colorscale = colorscales["Recovered"]
    elif y_axis == 'New Death':
        line_color =colors['text1']
        colorscale = colorscales["Death"]
    else:
        line_color = "white"
        colorscale = colorscales["Confirmed"]

    # Customizing y-axis ticks labels
    y_ticks = ["Week "+ str(s) for s in weeknumber_of_dates]

    # Creating hover text
    hover_text = ["Country: "+ option +"<br>"+"Date: "+d.strftime("%x")+"<br>"+y_axis+
    " Cases: "+ "{:,d}".format(value) for d,value in zip(dates_in_year,z)] #gives something like list of strings like '2018-01-25' for each date. Used in data trace to make good hovertext.
    cell_text = [s.strftime("%x") for s in dates_in_year]

    # Creating the heatmap
    fig = go.Figure(data = go.Heatmap(
    		x = weekdays_in_year,
    		y = weeknumber_of_dates,
    		z = z,
    		text=hover_text,
    		hoverinfo="text",
    		xgap=3, # this
    		ygap=3, # and this is used to make the grid-like apperance
    		# showscale=False,
            colorscale = colorscale
    	))
    # Adding the date on top of the heatmap using scatter plot in text mode
    fig.add_trace(go.Scatter(
            x = weekdays_in_year,
            y = weeknumber_of_dates,
            hoverinfo = "none",
            text = cell_text,
            mode = 'text',
            textposition = "middle center",
            textfont=dict(
            # family="sans serif",
            size=12,
            color=line_color,

            )

    ))
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
    	# title='Calendar Heatmap for '+y_axis+" Cases",
    	# height=400,
    	xaxis=dict(
    		tickmode="array",
    		ticktext=["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"],
    		tickvals=[0,1,2,3,4,5,6],
    		title="Week Days",
            showline = False,
            showgrid = False,
            zeroline = False
    	),
    	yaxis=dict(
            ticktext= y_ticks,
    		tickvals= list(weeknumber_of_dates),
    		showline = False,
            showgrid = False,
            zeroline = False,
    		title="Week Number"
    	),
    	plot_bgcolor=colors['graph_bg_color'], #making grid appear black
        font = dict(color = colors['text1'], size =12),
        # margin = dict(l=500,r=500,t=40,b=30),
        margin = dict(l=20,r=20),
        template = template,
        dragmode = False,
        # yaxis_nticks=len(set(months)),
        title_x= 0.5,
        titlefont= dict(
            color=colors['heading'],
            size=22
        ),
    )

    return fig

""" ###################################################
App Call Backs for TAB 4 - Weekly Forecast
###################################################"""

@app.callback(Output('forecast','figure'),
        [Input('tab-4-Dropdown1','value'),
        Input('tab-4-Dropdown2','value'),])
def update_figure(y_axis,countries):
    """
    Function to update line chart of estimated weekly forecast based on the
    the auto regression for the selected list of countries for the specific case type
    Arguments:
        y_axis: Dropdown value for the selected case
        countries: Dropdown value for the list of countries
    Returns:
        Updated line/scatter object based on the selected dropdown values and
        results of auto regression
    """

    countryAllDays_df = countryDays_df.loc[countryDays_df[y_axis] != 0].copy()
    countryAllDays_df = countryAllDays_df.sort_values(y_axis,ascending=False)
    selector_df = countryAllDays_df.groupby(["Country/Region"],as_index=False).agg({"Date":"first",y_axis:"max"})
    selector_df = selector_df.sort_values(y_axis,ascending=False)

    # selecting the countries based on the dropdown option
    if countries == "Top 10":
        limit = 10
        selected_countries = list(selector_df[:limit]['Country/Region'])
    elif countries == "G7":
        selected_countries = ['Canada','France','Germany','Italy','Japan','United Kingdom','US']
    elif countries == "BRICS":
        selected_countries = ['Brazil','Russia','India','China','South Africa']

    selected_df = countryAllDays_df[countryAllDays_df["Country/Region"].isin(selected_countries)]
    ordered_countries = list(selected_df['Country/Region'].unique())
    latest_date = df['Date'].max()
    next_week = []
    # Finding the dates of next week
    for x in range(1,8):
        next_day = latest_date+datetime.timedelta(days=x)
        next_week.append(next_day.date())

    selected_df['Date'] = pd.to_datetime(selected_df['Date'])
    selected_df = selected_df.sort_values([y_axis,'Date'],ascending=[False,True])


    # Drawing the line chart for the current figures
    fig = px.line(selected_df, x="Date", y=y_axis, color="Country/Region",
               hover_name="Country/Region")
    selected_df = selected_df.sort_values(y_axis,ascending=True)
    estimator = pd.DataFrame(columns = ['Country/Region','Date','Estimated '+y_axis])

    # Passing the current figures for each countries to auto regression forecat
    for country in ordered_countries:
        timeseries_df = selected_df[selected_df['Country/Region']==country]
        prediction = forecast(list(timeseries_df[y_axis]))
        row = []
        for i in range(len(next_week)):
            row.append([country + " Estimated",next_week[i],prediction[i]])
        copy =  pd.DataFrame(row,columns = ['Country/Region','Date','Estimated '+y_axis] )
        estimator = estimator.append(copy,ignore_index=True)
    row = []
    for country in ordered_countries:
        estimate = estimator[estimator['Country/Region']==country + " Estimated"]['Estimated '+y_axis].max()
        current = selected_df[selected_df['Country/Region']==country][y_axis].max()
        diff = int(estimate - current)
        row.append([country,diff])
    diff_df = pd.DataFrame(row,columns = ['Country/Region',y_axis])
    # Adding the estimated values for next week as scatter plot
    fig2 = px.scatter(estimator, x="Date", y='Estimated '+y_axis, color="Country/Region",
                   hover_name="Country/Region")

    for i in range(len(selected_countries)):
        fig.add_trace(fig2.data[i])

    # Adding shapes inside the graph to write custom text
    fig.add_shape(type="line",
            x0=selected_df['Date'].max(), x1=selected_df['Date'].max(), xref="x",
            y0=0, y1=estimator['Estimated '+y_axis].max(), yref="y",
            line = dict(color="salmon", width=1, dash="dot",)
    )
    fig.update_shapes(dict(xref='x', yref='y'))
    fig.add_shape(
            # filled Rectangle
                type="rect", x0=0.125,y0=0.63,x1=0.8,y1=0.95,xref="paper",yref="paper",
                line=dict(
                    color="#A21010",
                    width=1,
                ),
                fillcolor="#D6D8D5",
            )

    fig.add_annotation( # add a text callout with arrow saying 'Forecast begins!'
        text="Forecast begins!",
        x=selected_df['Date'].max(),
        y=estimator['Estimated '+y_axis].max()/2, arrowhead=1, showarrow=True
    )
    # Adding text inside the custom shapes on the graph
    # to add the top 3 countries based on the next week estimation
    fig.add_annotation( x=0.15, y=0.9, showarrow=False,
        text= "Highest Estimated* "+y_axis+" Cases for Next Week" ,
        xref="paper", yref="paper",bordercolor='#A21010',
            borderwidth=1, font=dict(
                color="white",
                size=16,
            ),bgcolor="#A21010",
    )
    axes = [0.84,0.79,0.74]
    diff_df = diff_df.sort_values(y_axis,ascending = False)
    for i in range(len(axes)):
        fig.add_annotation( x=0.15, y=axes[i], showarrow=False,
            text= str(i+1) + ". "+list(diff_df['Country/Region'])[i] + ":  " + str("{:,d}".format(list(diff_df[y_axis])[i])) ,
            xref="paper", yref="paper",
            font=dict(
                color="#A21010",
                size=18
            ),
        )
    fig.add_annotation( x=0.15, y=0.69, showarrow=False,
        text= "* In "+ countries + " Countries" ,
        xref="paper", yref="paper",
        font=dict(
            color="#525252",
            size=14
        ))

    fig.update_layout(
    title= countries +" Countries : "+y_axis+" Cases",
    template = template,
    dragmode = False,
    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],
    title_x= 0.5,

    titlefont= dict(
        color=colors['heading'],
        size=22
    ),

    margin=dict(l=60, r=20, t=80, b=20, autoexpand = True))
    return fig

# @app.callback(Output('moving-average','figure'),
#         [Input('tab-4-scale','value'),
#         Input('tab-4-Dropdown4','value')])
# def update_figure(scale, y_axis):
#     """
#     Function to update the subplots of line charts based on the
#     moving average of new cases based on the selected case type by the dropdown
#     on a linear/log scale selected by the radio button
#     Arguments:
#         y_axis: Dropdown value for the selected case
#         scale: Radio button value for the y_axis scale type
#     Returns:
#         Updated subplot object for the selected dropdown/radio button values
#     """
#     total_cases = y_axis
#     new_cases = "New "+y_axis
#
#     # Selecting the source dataframe
#     selected_df =  countryDays_df[['Country/Region','Date','Confirmed','Death',
#         'Recovered','New Confirmed','New Death','New Recovered']]
#     selector_df = latest_df.sort_values(total_cases,ascending=False)
#     selected_countries = list(selector_df[:10]['Country/Region'])
#     # Selecting the rows only for the top 10 countries
#     movingAvg_df = selected_df[selected_df["Country/Region"].isin(selected_countries)]
#     movingAvg_df = movingAvg_df.sort_values(['Country/Region','Date'], ascending = True)
#     ordered_countries = list(movingAvg_df['Country/Region'].unique())
#     # Initializing a dataframe for estimator dataframe
#     estimator = pd.DataFrame(columns = ['Country/Region','Date',total_cases, new_cases])
#     prediction = []
#
#     # Finding the 7-day moving average values for each countries
#     for country in ordered_countries:
#         timeseries_df = movingAvg_df[movingAvg_df['Country/Region']==country]
#         prediction.extend(list(timeseries_df.iloc[:,-1].rolling(window=7).mean()))
#     movingAvg_df['Moving Average'] = np.array(prediction)
#     movingAvg_df.fillna(0, inplace=True)
#
#     fig = make_subplots(rows=2, cols=5, specs=[[{},]*5,[{},]*5], shared_xaxes=False,
#                     shared_yaxes=False, vertical_spacing=0.1,)
#
#     i=1
#     c=1
#     # Adding the first 5 countries in the first row of subplot
#     for country in selected_countries[0:5]:
#         each_df = movingAvg_df[movingAvg_df['Country/Region']==country]
#         # Preparing custom hover text
#         my_text = [country+'<br><br>Moving Avg '+new_cases+': '+'{:,d} '.format(int(movingavg))+
#         '<br>Latest '+new_cases+' Cases: '+'{:,d}'.format(new)+
#         '<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+
#         '<br>Deaths:'+'{:,d}'.format(deaths)+
#         '<br>Recovered: '+'{:,d}'.format(recovered)+
#       "<extra></extra>"
#       for country,movingavg,new,confirmed, deaths, recovered
#         in zip(list(each_df['Country/Region']), list(each_df['Moving Average']),
#         list(each_df['New Confirmed']),  list(each_df['Confirmed']),
#          list(each_df['Death']), list(each_df['Recovered']))]
#         if i==1:
#             fig.append_trace(go.Scatter(
#                                         x=each_df[total_cases],
#                                         y=each_df[new_cases],
#                                         mode="lines+markers",
#                                         name = country,
#                                         xaxis = 'x',
#                                         yaxis = 'y',
#                                         hovertemplate = my_text,
#                                     ), row=1, col=i)
#         else:
#             fig.append_trace(go.Scatter(
#                                     x=each_df[total_cases],
#                                     y=each_df[new_cases],
#                                     mode="lines+markers",
#                                     name = country,
#                                     xaxis = 'x'+str(c),
#                                     yaxis='y'+str(c),
#                                     hovertemplate = my_text,
#                                 ), row=1, col=i)
#         i += 1
#         c += 1
#     i=1
#     c=5
#
#     # Adding the next 5 countries in the second row of subplot
#     for country in selected_countries[5:]:
#         each_df = movingAvg_df[movingAvg_df['Country/Region']==country]
#         # Preparing custom hover text
#         my_text = [country+'<br><br>Moving Avg '+new_cases+': '+'{:,d}'.format(int(movingavg))+
#         '<br>Latest '+new_cases+' Cases: '+'{:,d}'.format(new)+
#         '<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+
#         '<br>Deaths:'+'{:,d}'.format(deaths)+
#         '<br>Recovered: '+'{:,d}'.format(recovered)+
#       "<extra></extra>"
#       for country,movingavg,new,confirmed, deaths, recovered
#         in zip(list(each_df['Country/Region']), list(each_df['Moving Average']),
#         list(each_df['New Confirmed']),  list(each_df['Confirmed']),
#          list(each_df['Death']), list(each_df['Recovered']))]
#
#         fig.append_trace(go.Scatter(
#                                     x=each_df[total_cases],
#                                     y=each_df[new_cases],
#                                     mode="lines+markers",
#                                     name = country,
#                                     xaxis = 'x'+str(c),
#                                     yaxis='y'+str(c),
#                                     hovertemplate = my_text,
#                                 ), row=2, col=i)
#         i += 1
#         c += 1
#
#     xaxes = [0.02,0.22,0.45,0.66,0.89]
#     yaxes = [0.98,0.38]
#
#     c = 0
#     # Adding Country names as titles using figure annotations
#     for i in range(len(xaxes)):
#         fig.add_annotation( x=xaxes[i], y=yaxes[0], showarrow=False,
#             text= selected_countries[c], xref="paper", yref="paper",
#             font=dict(color=colors['graph_text'], size=18))
#         c+=1
#     # c = 5
#     for i in range(len(xaxes)):
#         fig.add_annotation( x=xaxes[i], y=yaxes[1], showarrow=False,
#             text= selected_countries[c], xref="paper", yref="paper",
#             font=dict(color=colors['graph_text'], size=18))
#         c+=1
#     # Updating the layout of graph based on the y_axis scale selected by dropdown
#     fig.update_layout(
#     title= "Top 10 Countries : "+new_cases+" Cases Vs "+total_cases,
#     xaxis= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis2= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis3= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis4= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis5= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis6= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis7= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis8= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis9= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     xaxis10= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis2= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis3= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis4= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis5= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis6= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis7= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis8= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis9= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#     yaxis10= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
#
#
#     paper_bgcolor=colors['graph_bg_color'],
#     plot_bgcolor=colors['graph_bg_color'],
#     title_x= 0.5,
#     template = template,
#     # yaxis_type="log",
#     titlefont= dict(
#         color=colors['heading'],
#         size=22
#     ),
#     # title_y = 0.05,
#     margin=dict(l=60, r=20, t=80, b=20, autoexpand = True))
#
#     return fig
@app.callback(Output('moving-average','figure'),
        [Input('tab-4-scale','value'),
        Input('tab-4-Dropdown4','value')])
def update_figure(scale, y_axis):
    """
    Function to update the subplots of line charts based on the
    moving average of new cases based on the selected case type by the dropdown
    on a linear/log scale selected by the radio button
    Arguments:
        y_axis: Dropdown value for the selected case
        scale: Radio button value for the y_axis scale type
    Returns:
        Updated subplot object for the selected dropdown/radio button values
    """
    total_cases = y_axis
    new_cases = "New "+y_axis

    # Selecting the source dataframe
    selected_df =  countryDays_df[['Country/Region','Date','Confirmed','Death',
        'Recovered','New Confirmed','New Death','New Recovered']]
    selector_df = latest_df.sort_values(total_cases,ascending=False)
    selected_countries = list(selector_df[:10]['Country/Region'])
    # Selecting the rows only for the top 10 countries
    movingAvg_df = selected_df[selected_df["Country/Region"].isin(selected_countries)]
    movingAvg_df = movingAvg_df.sort_values(['Country/Region','Date'], ascending = True)
    ordered_countries = list(movingAvg_df['Country/Region'].unique())
    # Initializing a dataframe for estimator dataframe
    estimator = pd.DataFrame(columns = ['Country/Region','Date',total_cases, new_cases])
    prediction = []

    # Finding the 7-day moving average values for each countries
    for country in ordered_countries:
        timeseries_df = movingAvg_df[movingAvg_df['Country/Region']==country]
        # prediction.extend(list(timeseries_df.iloc[:,-1].rolling(window=7).mean()))
        prediction.extend(list(timeseries_df[new_cases].rolling(window=7).mean()))
    movingAvg_df['Moving Average'] = np.array(prediction)
    movingAvg_df.fillna(0, inplace=True)

    fig = make_subplots(rows=3, cols=3, specs=[[{},]*3,[{},]*3,[{},]*3], shared_xaxes=False,
                    shared_yaxes=False, vertical_spacing=0.1,)

    i=1
    c=1
    # Adding the first 5 countries in the first row of subplot
    for country in selected_countries[0:3]:
        each_df = movingAvg_df[movingAvg_df['Country/Region']==country]
        # Preparing custom hover text
        my_text = [country+'<br><br>Moving Avg '+new_cases+': '+'{:,d} '.format(int(movingavg))+
        '<br>'+new_cases+' Cases: '+'{:,d}'.format(new)+
        '<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+
        '<br>Deaths:'+'{:,d}'.format(deaths)+
        '<br>Recovered: '+'{:,d}'.format(recovered)+
      "<extra></extra>"
      for country,movingavg,new,confirmed, deaths, recovered
        in zip(list(each_df['Country/Region']), list(each_df['Moving Average']),
        list(each_df[new_cases]),  list(each_df['Confirmed']),
         list(each_df['Death']), list(each_df['Recovered']))]
        if i==1:
            fig.append_trace(go.Scatter(
                                        x=each_df[total_cases],
                                        y=each_df['Moving Average'],
                                        mode="lines+markers",
                                        name = country,
                                        xaxis = 'x',
                                        yaxis = 'y',
                                        hovertemplate = my_text,
                                    ), row=1, col=i)
        else:
            fig.append_trace(go.Scatter(
                                    x=each_df[total_cases],
                                    y=each_df['Moving Average'],
                                    mode="lines+markers",
                                    name = country,
                                    xaxis = 'x'+str(c),
                                    yaxis='y'+str(c),
                                    hovertemplate = my_text,
                                ), row=1, col=i)
        i += 1
        c += 1
    i=1
    c=4

    # Adding the next 5 countries in the second row of subplot
    for country in selected_countries[3:6]:
        each_df = movingAvg_df[movingAvg_df['Country/Region']==country]
        # Preparing custom hover text
        my_text = [country+'<br><br>Moving Avg '+new_cases+': '+'{:,d}'.format(int(movingavg))+
        '<br>'+new_cases+' Cases: '+'{:,d}'.format(new)+
        '<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+
        '<br>Deaths:'+'{:,d}'.format(deaths)+
        '<br>Recovered: '+'{:,d}'.format(recovered)+
      "<extra></extra>"
      for country,movingavg,new,confirmed, deaths, recovered
        in zip(list(each_df['Country/Region']), list(each_df['Moving Average']),
        list(each_df[new_cases]),  list(each_df['Confirmed']),
         list(each_df['Death']), list(each_df['Recovered']))]

        fig.append_trace(go.Scatter(
                                    x=each_df[total_cases],
                                    y=each_df['Moving Average'],
                                    mode="lines+markers",
                                    name = country,
                                    xaxis = 'x'+str(c),
                                    yaxis='y'+str(c),
                                    hovertemplate = my_text,
                                ), row=2, col=i)
        i += 1
        c += 1

    i = 1
    c=7
    # Adding the next 5 countries in the second row of subplot
    for country in selected_countries[6:9]:
        each_df = movingAvg_df[movingAvg_df['Country/Region']==country]
        # Preparing custom hover text
        my_text = [country+'<br><br>Moving Avg '+new_cases+': '+'{:,d}'.format(int(movingavg))+
        '<br>'+new_cases+' Cases: '+'{:,d}'.format(new)+
        '<br>Confirmed Cases: '+'{:,d}'.format(confirmed)+
        '<br>Deaths:'+'{:,d}'.format(deaths)+
        '<br>Recovered: '+'{:,d}'.format(recovered)+
      "<extra></extra>"
      for country,movingavg,new,confirmed, deaths, recovered
        in zip(list(each_df['Country/Region']), list(each_df['Moving Average']),
        list(each_df[new_cases]),  list(each_df['Confirmed']),
         list(each_df['Death']), list(each_df['Recovered']))]

        fig.append_trace(go.Scatter(
                                    x=each_df[total_cases],
                                    y=each_df['Moving Average'],
                                    mode="lines+markers",
                                    name = country,
                                    xaxis = 'x'+str(c),
                                    yaxis='y'+str(c),
                                    hovertemplate = my_text,
                                ), row=3, col=i)
        i += 1
        c += 1

    xaxes = [0.015,0.41,0.79]
    yaxes = [0.99,0.60 ,0.2225]

    c = 0
    # Adding Country names as titles using figure annotations
    for i in range(len(xaxes)):
        fig.add_annotation( x=xaxes[i], y=yaxes[0], showarrow=False,
            text= selected_countries[c], xref="paper", yref="paper",
            font=dict(color=colors['graph_text'], size=18))
        c+=1
    c = 4

    for i in range(len(xaxes)):
        fig.add_annotation( x=xaxes[i], y=yaxes[1], showarrow=False,
            text= selected_countries[c], xref="paper", yref="paper",
            font=dict(color=colors['graph_text'], size=18))
        c+=1
    c = 7
    for i in range(len(xaxes)):
        fig.add_annotation( x=xaxes[i], y=yaxes[2], showarrow=False,
            text= selected_countries[c], xref="paper", yref="paper",
            font=dict(color=colors['graph_text'], size=18))
        c+=1
    # Updating the layout of graph based on the y_axis scale selected by dropdown
    fig.update_layout(
    title= "Top 9 Countries : Moving Avg of "+new_cases+" Cases Vs "+total_cases,
    xaxis= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis2= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis3= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis4= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis5= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis6= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis7= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis8= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    xaxis9= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    # xaxis10= {'title': total_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis2= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis3= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis4= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis5= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis6= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis7= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis8= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    yaxis9= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},
    # yaxis10= {'title': new_cases, 'type' : 'linear' if scale == 'Linear' else 'log'},


    paper_bgcolor=colors['graph_bg_color'],
    plot_bgcolor=colors['graph_bg_color'],
    title_x= 0.5,
    template = template,
    # yaxis_type="log",
    titlefont= dict(
        color=colors['heading'],
        size=22
    ),
    # title_y = 0.05,
    margin=dict(l=60, r=20, t=80, b=20, autoexpand = True))

    return fig

# """ ###################################################
# App Call Backs for TAB 5 - COVID Research Data clustering
# ###################################################"""
#
# @app.callback(Output('scatter_cluster','figure'),
#         [Input('tab-5-option1','value')])
# def update_figure(cluster_num):
#     """
#     Function to update scatter plot of clusters for single level clustering
#      based on the dropdown value  for cluster number
#     Arguments:
#         cluser_num: Dropdown value for the number of clusters
#     Returns:
#         Updated scatter plot object for the selected number of clusters
#     """
#
#     if cluster_num == "5 Clusters":
#         k = 5
#     elif cluster_num == "10 Clusters":
#         k = 10
#     else:
#         k = 15
#
#     # Loading in single level cluster input
#     X_embedded_child = scatter_data(k)
#     X_cordinate=[[] for _ in range(k)]
#     Y_cordinate=[[] for _ in range(k)]
#     AVX,AVY,size,a= [],[],[],[]
#     fig = go.Figure()
#
#      # seperating the position of each cluster for using in plotly
#     for i in range (0,k):
#         data=X_embedded_child[i]
#         for ii in data:
#             X_cordinate[i].append(ii[0])
#             Y_cordinate[i].append(ii[1])
#
#         # Adding each cluster points separately to the plot
#         fig.add_trace(go.Scatter(x=X_cordinate[i], y=Y_cordinate[i], mode='markers',
#                 marker=dict(size=5,line=dict(width=0.25,color='black')),
#                 name = "Cluster "+str(i+1),
#                 text = "Cluster "+str(i+1),
#                 hoverinfo = "text",
#                 ))
#     fig.update_layout(
#         title = "Scatter Plot for "+cluster_num,
#         title_x= 0.5,
#         titlefont= dict(
#             color=colors['heading'],
#             size=18
#         ),
#         template = template,
#         margin=dict(l=10, r=10),
#         paper_bgcolor=colors['graph_bg_color'],
#         plot_bgcolor=colors['graph_bg_color'],)
#
#     return fig
#
# @app.callback(Output('bubble_cluster','figure'),
#         [Input('tab-5-option1','value')])
# def update_figure(cluster_num):
#     """
#     Function to update bubble plot for single level clustering data
#      where the coordinates are centroid of clusters and size is count of
#      articles in each clusters
#     Arguments:
#         cluser_num: Dropdown value for the number of clusters
#     Returns:
#         Updated bubble plot object for the selected number of clusters
#     """
#
#     if cluster_num == "5 Clusters":
#         k = 5
#     elif cluster_num == "10 Clusters":
#         k = 10
#     else:
#         k = 15
#     # Loading in the cluster input data
#     X_embedded_child = scatter_data(k)
#
#     X_cordinate=[[] for _ in range(k)]
#     Y_cordinate=[[] for _ in range(k)]
#     AverageX,AverageY,size,a= [],[],[],[]
#     fig = go.Figure()
#
#     # Separating X and y coordinates to plot the bubble plot
#     # and finding the mean of coordinates for each cluster
#     for i in range (0,k):
#         data=X_embedded_child[i]
#         size.append(len(X_embedded_child[i])/50)
#         for ii in data:
#             X_cordinate[i].append(ii[0])
#             Y_cordinate[i].append(ii[1])
#         mean_X=np.mean(X_cordinate[i])
#         mean_Y=np.mean(Y_cordinate[i])
#         AverageX.append(mean_X)
#         AverageY.append(mean_Y)
#
#     # Appending the size of each cluster to a list
#     for i in range (0,len(size)):
#         a.append(i)
#     clusters = ["Cluster " + str(a+1) for a in range(0,k)]
#     # Creating the bubble plot for centroids
#     fig = go.Figure(data=go.Scatter(x=AverageX,y=AverageY,mode='markers',
#                     text = clusters,
#                     hoverinfo = "text",
#                     marker=dict(size=size,
#                             # sizemode='area',
#                             # sizeref=2.*max(size)/(40.**2),
#                             sizemin=4,
#                             color=a)))
#
#
#     fig.update_layout(
#         title = "Bubble Plot for "+cluster_num,
#         title_x= 0.5,
#         titlefont= dict(
#             color=colors['heading'],
#             size=18
#         ),
#         template = template,
#         margin=dict(l=10, r=10),
#         paper_bgcolor=colors['graph_bg_color'],
#         plot_bgcolor=colors['graph_bg_color'],)
#
#     return fig
#
# @app.callback(Output('sunburst1','figure'),
#         [Input('tab-5-option2','value')])
# def update_figure(cluster_num):
#     """
#     Function to update sunburst for single level clustering data
#      based on the number of clusters selected by dropdown
#     Arguments:
#         cluser_num: Dropdown value for the number of clusters
#     Returns:
#         Updated sunburst object for the selected number of clusters
#     """
#
#     if cluster_num == "5 Clusters":
#         k = 5
#     elif cluster_num == "10 Clusters":
#         k = 10
#     else:
#         k = 15
#     colorscale = "rdbu"
#
#     # Loading the single level clustering data
#     y_pred5 = sunburst_single(k)
#
#     # Getting the article list from the covid research dataframe
#     article=list(df_covid["title"])[1:100]
#     # Getting the clusters
#     cluster = [x + 1 for x in list(y_pred5[1:100])]
#     # Getting the clusters
#     value = [x + 1 for x in list(y_pred5[1:100])]
#     # Stacking different levels of hierarchy to create a dataframe out of it
#     data = np.dstack([article, cluster,value]).reshape(99,3)
#     df = pd.DataFrame(data,columns = ['article','cluster','value'])
#
#     # Creating the sunburst
#     fig =px.sunburst(df, path=['cluster','article'] ,values='value',
#                         color_continuous_scale=colorscale,)
#
#
#     fig.update_layout(
#         title = "Single Level Clustering for "+cluster_num,
#         title_x= 0.5,
#         titlefont= dict(
#             color=colors['heading'],
#             size=18
#         ),
#         template = template,
#         margin=dict(l=10, r=10),
#         paper_bgcolor=colors['graph_bg_color'],
#         plot_bgcolor=colors['graph_bg_color'],)
#
#     return fig
#
#
# def takeSecond(elem):
#     """
#     Function to return the second element of a list
#     """
#     return elem[1]
#
#
# @app.callback(Output('sunburst2','figure'),
#         [Input('tab-5-option3','value')])
# def update_figure(cluster_num):
#     """
#     Function to update sunburst for multi level clustering data
#      based on the number of parent-child clusters selected by dropdown
#     Arguments:
#         cluser_num: Dropdown value for the parent-child clusters
#     Returns:
#         Updated sunburst object for the selected number of clusters
#     """
#
#     if cluster_num == "5 Parents-5 Child Clusters":
#         k = 5
#     else:
#         k = 10
#     colorscale = "rdbu"
#
#     # Loading the first level and second level cluster data
#     y_pred5 = sunburst_single(5)
#     second = sunburst_multi(k)
#
#     data_sort=[]
#
#     # Getting the article titles of COVID research data
#     data=df_covid['title']
#     x_array_title=np.array(data)
#
#     # Sortng the cluster dataset
#     for i in range (0,700) :
#        x=x_array_title[i]
#        y=y_pred5[i]
#        data_sort.append((x,y))
#        (data_sort).sort(key=takeSecond)
#
#     x_cordinate,y_cordinate=[],[]
#     for i in data_sort:
#        (x_cordinate).append((i[0][:]))
#        (y_cordinate).append((i[:][1]))
#     second_array=[]
#     # Getting the second level of clustering
#     for i in second:
#         for ii in i:
#             second_array.append(ii)
#     np.transpose(second_array)
#
#     fig = go.Figure()
#
#     # Getting the article titles
#     article = x_cordinate
#     # Getting the first level of clustering (parent)
#     cluster = [a + 1 for a in y_cordinate]
#     # Getting the second level of clustering (child)
#     cluster2 = [a + 1 for a in second_array[0:700]]
#     value = cluster2
#     # Stacking each level to create dataframe for the plot
#     data = np.dstack([article, cluster, cluster2,value]).reshape(700,4)
#     df = pd.DataFrame(data,columns = ['article','cluster','cluster2','value'])
#
#     # Creating the sunburst
#     fig =px.sunburst(
#        df, path=['cluster','cluster2','article'] ,values='value',
#                                color_continuous_scale=colorscale,)
#
#     fig.update_layout(
#         title = "Multi-Level Clustering for "+cluster_num,
#         title_x= 0.5,
#         titlefont= dict(
#             color=colors['heading'],
#             size=18
#         ),
#         template = template,
#         margin=dict(l=10, r=10),
#         paper_bgcolor=colors['graph_bg_color'],
#         plot_bgcolor=colors['graph_bg_color'],)
#     return fig
#
# @app.callback(Output('dendrogram1','figure'),
#         [Input('tab-5-option4','value')])
# def update_figure(cluster_num):
#     """
#     Function to update dendrogram for multi level clustering data
#      based on the number of parent-child clusters selected by dropdown
#     Arguments:
#         cluser_num: Dropdown value for the number of parent-child clusters
#     Returns:
#         Updated dendrogram object for the selected number of parent-child clusters
#     """
#
#     if cluster_num == "5 Parents-5 Child Clusters":
#         k = 5
#     else:
#         k = 10
#
#     # Loading in the first level and second level cluster input
#     y_pred5 = sunburst_single(5)
#     second = sunburst_multi(k)
#
#     data_sort=[]
#
#     # Getting the article title from COVID research dataframe
#     data=df_covid['title']
#     x_array_title=np.array(data)
#
#     # Sorting the data in order
#     for i in range (0,700) :
#        xx_array_title=x_array_title[i]
#        y=y_pred5[i]
#        data_sort.append((xx_array_title,y))
#        data_sort.sort(key=takeSecond)
#
#     x_cordinate,y_cordinate=[],[]
#     # Separating the X and Y coordinates
#     for i in data_sort:
#        x_cordinate.append((i[0][:]))
#        y_cordinate.append((i[:][1]))
#     second_cluster_order=[]
#     # Creating the second level cluster in order
#     for i in second:
#         for ii in i:
#             second_cluster_order.append(ii)
#     np.transpose(second_cluster_order)
#
#     sec_order=(y_cordinate,second_cluster_order[0:700])
#     clusters=[]
#     # separating the x ad y values of clusters for plotting
#     for i in range (0,700):
#         x1=sec_order[0][i]
#         y1=sec_order[1][i]
#         clusters.append((x1,y1))
#
#     fig = go.Figure()
#     clusters_array = np.array(clusters)
#     names = x_cordinate[0:200]#
#
#     # Creating dendrogram
#     fig = ff.create_dendrogram(clusters_array[0:200], orientation='left', labels=names)
#     fig.update_layout(
#         title = "Dendrogram  for "+cluster_num,
#         title_x= 0.5,
#         titlefont= dict(
#             color=colors['heading'],
#             size=18
#         ),
#         template = template,
#         # margin=dict(l=10, r=10),
#         paper_bgcolor=colors['graph_bg_color'],
#         plot_bgcolor=colors['graph_bg_color'],)
#     return fig

if __name__ == '__main__':
    app.run_server(debug = False)
    #app.server.run(port=8000, host='127.0.0.1')
