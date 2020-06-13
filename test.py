#Packages
from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import locale
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Set Currency Locale
locale.setlocale( locale.LC_ALL, '' )

# Base path to data files
base_path = Path(__file__).resolve().parent / "data"
census_path = base_path / "census_data"
hud_path = base_path / "hud_prog_data"
chas_path = base_path / "CHAS_data"
pop_path =  base_path / "pop_proj" / "hist_d"

#Current Pop Data
today = pd.read_csv(str(base_path /"today.csv"))

#ACS DP02-05 Data
df = pd.read_csv(str(census_path /"acs5_dp04.csv"))
dp = pd.read_csv(str(census_path / "acs5_dp02.csv"))
ep = pd.read_csv(str(census_path / "acs5_dp03.csv"))
tp = pd.read_csv(str(census_path / "acs5_dp05.csv"))

#App Creation
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Raleway&display=swap",
    "https://fonts.googleapis.com/css2?family=Raleway&family=Roboto&display=swap"
]
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
server = app.server
app.title = 'Housing Profile Dashboard'

# No data layout
no_data_fig = { 
    "layout":
        {
            "xaxis": { "visible": False },
            "yaxis": { "visible": False },
            "annotations": [
                    {
                        "text": "No data available",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": { "size": 28 }
                    }
                ]
        }
}

#App Layout
app.layout = html.Div([
    html.Div(
    className="app-header",
    children=[
        html.Div('Housing Profile Dashboard', className="app-header--title")
        ]
    ),
    html.Div(
        className='dropdown',
        children = [    
            html.Label("Select Location :"),
            html.Div(dcc.Dropdown(
                id='demo-dropdown',
                options=[{"label":c, "value":c} for c in sorted(df['County Name'])],
                placeholder = "Select a County...",
                value='Contra Costa County, California'),
                className = 'dropdown--lister')
        ]
    ),
    html.Div(
        className = 'c-profile',
        children=[
            html.Div(id = 'county-name', className="c-profile--title")
            ]
        ),
    html.Div(
            className = 'row two columns',
            children = [
            html.Div(
                className = 'box',
                children = [  
                    html.Div([
                        dcc.Graph(id = 'age-g'),
                    ]),
                ]    
            ),
    ]),
])

##County Proflie Name Control
@app.callback(
    dash.dependencies.Output('county-name', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def cvup(value):
    return 'Housing Profile: {}'.format(value)

##Population by Age
@app.callback(
    dash.dependencies.Output('age-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_ages(value):
    ###Pull and Collate Data
    females = today[today.sex == 'Female']
    males = today[today.sex == 'Male']
    age = list(females['age'])
    female_pop = list(females[value])
    male_pop = list(males[value])
    age1 = age
    
    ###Create Graph
    fig10 = fig = make_subplots(shared_xaxes=False,
                    shared_yaxes=True, vertical_spacing=0.001)
    fig10.append_trace(go.Bar(
        x=female_pop,
        y=age,
        marker=dict(
            color='rgba(28,41,91, 1.0)',
            line=dict(
                color='rgba(3,18,73, 1.0)',
                width=1),
        ),
        name='Female Population',
        orientation='h',
    ), 1, 1)
    fig10.append_trace(go.Bar(
        x=male_pop,
        y=age1,
        marker=dict(
            color='rgba(78,89,127, 1.0)',
            line=dict(
                color='rgba(53,65,109, 1.0)',
                width=1),
        ),
        name='Male Population',
        orientation='h',
    ), 1, 1)
    fig10.update_yaxes(autorange="reversed")
    fig10.update_layout(
    title='Population Tree',
    autosize=False,
    legend=dict(x=.25, y=1.3, font_size=10),
    width=800, 
    height=450,
    xaxis2=dict(
        autorange="reversed",
    )
    )
    fig10.update_xaxes(nticks=10)   
    return fig10


if __name__ == '__main__':
    app.run_server(debug=True)
