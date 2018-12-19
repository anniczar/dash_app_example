#!/usr/bin/env python
# coding: utf-8

# In[5]:


import dash
#to create apps 
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('nama_10_gdp_1_Data.csv', na_values=':',usecols=["TIME","UNIT","GEO","NA_ITEM","Value"])
df['Value']=df['Value'].str.replace(',','').astype(float)
df=df.dropna()

#~ for dropping values

df=df[~df.GEO.str.contains("Eur") ==True]
df=df[~df.UNIT.str.contains("Current prices, million euro")]
df=df[~df.UNIT.str.contains("Chain linked volumes, index 2010=100")]







print(df.head())


# In[2]:


#define dropdown list
available_indicators = df['NA_ITEM'].unique()
GEOS=df['GEO'].unique()
app.layout = html.Div([
    html.Div([

        html.Div([
           dcc.Dropdown(        #dropdown menu for x axis
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([    
            dcc.Dropdown(          #dropdown menu for y axis
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )   
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'), 

    
#insert slider for different years 
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    html.H1('\n'), #line break

    html.Div([
        html.Div([
            dcc.Dropdown( #dropdown for content displayed
                id='country',
                options=[{'label': i, 'value': i} for i in GEOS],
                value='European Union (current composition)'
            ),
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([ #dropdown for y axis
            dcc.Dropdown(
                id='yaxis-column-b',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic-b')
    
])

@app.callback(   #code that is passed as an argument to other code that is expected to call back (execute) the argument at a given time.
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type','value'),
     dash.dependencies.Input('yaxis-type','value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['NA_ITEM'] == xaxis_column_name) &( dff['GEO']==str(i) )]['Value'],
            y=dff[(dff['NA_ITEM'] == yaxis_column_name) &( dff['GEO']==str(i))]['Value'],
            text=dff[dff['GEO']==str(i)]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i[:20]
            
        )for i in dff.GEO.unique()
                ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic-b', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis-column-b', 'value')])
def update_graph_b(country_name, yaxis_column_b_name,):
    dff = df[df['GEO'] == country_name]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == yaxis_column_b_name]['TIME'],
            y=dff[dff['NA_ITEM'] == yaxis_column_b_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_b_name]['Value'],
            mode='lines'
            
            
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'YEAR',
                'type': 'linear' 
            },
            yaxis={
                'title': yaxis_column_b_name,
                'type': 'linear' 
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()


# In[ ]:




