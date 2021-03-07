#Packages
from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import locale
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import urllib
from future.standard_library import install_aliases
install_aliases()
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

#Set Currency Locale and latest year
locale.setlocale( locale.LC_ALL, '' )
year = 2019
hudpictureyear = 2020
chasyear = '2013-2017'

# Base path to data files
base_path = Path(__file__).resolve().parent / "data"
census_path = base_path / "census_data"
hud_path = base_path / "hud_prog_data"
chas_path = base_path / "CHAS_data"
pop_path =  base_path / "pop_proj" / "hist_d"
asset_path = base_path / "assets"

#Data
data = pd.read_csv(str(base_path /"dashdata.csv"))
csvdownload = pd.read_csv(str(base_path /"csvdownload.csv"))

#HUD Program and LIHTC Data
hud1 = pd.read_csv(str(hud_path / "hudunits.csv"))
litc = pd.read_csv(str(hud_path / "lihtc.csv"))

#Historical Pop Data
hist = pd.read_csv(str(pop_path / "h_pop.csv"))

#Option Lists
monthly_options = ['Household Income', 'Monthly Rent', 'Monthly Homeowner Costs (Mortgage)', 'Monthly Homeowner Costs (No Mortgage)']

#App Creation
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Raleway&display=swap",
    "https://fonts.googleapis.com/css2?family=Raleway&family=Roboto&display=swap",
    "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
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
    html.Div(className = 'headgridcontainer',
            children = [
                html.Div(className='hbox item1',
                children = [
                    html.Div('Housing Profile Dashboard', className="apptitle"),
                    html.Div(className='titleunderline')
            ]),
            html.Div(className='hbox item2',
                children = [
                    html.Div(id = 'county-name', className="apptitle"),
                    html.A('Download Data',id='download-link',download="rawdata.csv", href="",target="_blank",
                    className = 'download'),
                    
            ]),
            html.Div(className='hbox item3',
                children = [
                    html.Div(dcc.Dropdown(
                        id='demo-dropdown',
                        options=[{"label":c, "value":c} for c in sorted(data['NAME'])],
                        placeholder = "Select a County...",
                        value='Contra Costa County, California',),
                        className = 'dropdown--lister'),
            ]),
    ]),
    html.Div(className='spacer'),
    html.Div(className = 'cards',
            children =[
                html.Div(className='card',
                children = [
                    html.Div(id='totalpopulation', className = 'cardtitle'),
                    html.Div(className = 'cardcap'),
                    html.Div('Total Population', className = 'cardlabel'),
                ]),
                html.Div(className='card',
                children = [
                    html.Div(id='totalhouseholds', className = 'cardtitle'),
                    html.Div(className = 'cardcap'),
                    html.Div('Households', className = 'cardlabel'),
                ]),
                html.Div(className='card',
                children = [
                    html.Div(id='totalhousing', className = 'cardtitle'),
                    html.Div(className = 'cardcap'),
                    html.Div('Housing Units', className = 'cardlabel'),
                ]),

    ]),
    html.Div(className='spacer'),
    html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', parent_className='custom-tabs', className='custom-tabs-container', 
        children=[
        dcc.Tab(label='Housing Inventory', value='tab-1', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label='Housing Affordability', value='tab-2', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label = 'Housing Demand', value = 'tab-3', className='custom-tab', selected_className='custom-tab--selected')
    ]),
    html.Div(id='tabs-example-content')
    ]),
    html.Div(className='spacer'),
    html.Div(
    className="app-footer",
    children=[
        html.Div('Housing Profile Dashboard v2.0: Produced By Devin McNally and Ryan McNally', className="app-footer--text"),
        html.Div('All data is collected and presented at no cost. If you use this, please attribute this project!', className="app-footer--text"),
        html.Div('Last Updated: February 28, 2021', className="app-footer--text")
        ]
    ),

])

##Tab Control    
@app.callback(
    dash.dependencies.Output('tabs-example-content', 'children'),
    [dash.dependencies.Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(className = 'spacer'),
            html.Div(className='tab1grid',
            children = [
                html.Div(
                    children = [
                    dcc.Graph(id = 'units-type'),
                    html.Div('U.S. Census Bureau, American Community Survey Table: DP04, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'span2box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'bed-t'),
                    html.Div('U.S. Census Bureau, American Community Survey Table: DP04, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'unit-age'),
                    html.Div('U.S. Census Bureau, American Community Survey Table: DP04, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'hud-units'),
                    html.Div('HUD Picture of Subsidized Households & Low-Income Housing Tax Credit Data Dataset, {}'.format(str(hudpictureyear)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'units-vacancy'),
                    html.Div('U.S. Census Bureau, American Community Survey Table: DP04, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
            ]),
        ]),
    elif tab == 'tab-2':
        return html.Div([
            html.Div(className = 'spacer'),
            html.Div(className='tab1grid',
            children = [
                html.Div(
                    children = [
                    html.Div(
                        dcc.Dropdown(
                                id='mdropdown',
                                options=[{"label":c, "value":c} for c in sorted(monthly_options)],
                                placeholder = 'Household Income',
                                value = 'Household Income'),
                                className = 'dropdown--lister'),
                    dcc.Graph(id = 'm-dist'),
                    html.Div('U.S. Census Bureau, American Community Survey Table: DP03 & DP04, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'span2box'),
                html.Div(
                    children = [
                    dbc.RadioItems(
                        id='rentradio',
                        options=[
                            {'label': 'Gross Gap', 'value': 'grossgap'},
                            {'label': 'Net Gap', 'value': 'netgap'},
                        ],
                        value='netgap',
                        className = 'radios'), 
                    dcc.Graph(id = 'rent-gap'),
                    html.Div('HUD CHAS Dataset, {}'.format(chasyear),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                    html.Div(
                    children = [
                    dbc.RadioItems(
                        id='homeradio',
                        options=[
                            {'label': 'Gross Gap', 'value': 'grossgap'},
                            {'label': 'Net Gap', 'value': 'netgap'},
                        ],
                        value='netgap',
                        className = 'radios'),
                    dcc.Graph(id = 'home-gap'),
                    html.Div('HUD CHAS Dataset, {}'.format(chasyear),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'hh-inc'),
                    html.Div('HUD CHAS Dataset, {}'.format(chasyear),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'hh-assist'),
                    html.Div('U.S. Census Bureau, American Community Survey Table: DP03, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
            ]),
        ])

    elif tab == 'tab-3':
        return html.Div([
            html.Div(className = 'spacer'),
            html.Div(className='tab1grid',
            children = [
                html.Div(
                    children = [
                    dcc.Graph(id = 'hist'),
                    html.Div('U.S. Census Bureau, Population of States and Counties of the United States: 1790 to 1990, Decennial Census SF1: 2000, ACS 2015 5-Year Estimates, ACS {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'age-g'),
                    html.Div('U.S. Census Bureau, American Community Survey Tables: B01001B-B01001I, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'race-g'),
                    html.Div('U.S. Census Bureau, American Community Survey Tables: B01001B-B01001I, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'hhsize'),
                    html.Div('U.S. Census Bureau, American Community Survey Tables: S2501, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tab1box'),
                html.Div(
                    children = [
                    dcc.Graph(id = 'spec-g'),
                    html.Div('U.S. Census Bureau, American Community Survey Tables: DP05, {} 5-Year Estimates'.format(str(year)),className='sourcelabel'),
                    ],
                    className = 'tabbbox'),
            ]),
        ]),




##County Proflie Name Control
@app.callback(
    dash.dependencies.Output('county-name', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def countyn_update(value):
    return '{}'.format(value)

##Top Cards
@app.callback(
    dash.dependencies.Output('totalpopulation', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def countyn_update(value):
    units = data[data['NAME'] == value]
    units = units[['Total Population']]
    value = units['Total Population'].iloc[0]
    return '{:,}'.format(round(value))


@app.callback(
    dash.dependencies.Output('totalhouseholds', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def countyn_update(value):
    units = data[data['NAME'] == value]
    units = units[['Total Households']]
    value = units['Total Households'].iloc[0]
    return '{:,}'.format(round(value))


@app.callback(
    dash.dependencies.Output('totalhousing', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def countyn_update(value):
    units = data[data['NAME'] == value]
    units = units[['Total Housing Units']]
    value = units['Total Housing Units'].iloc[0]
    return '{:,}'.format(round(value))


@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_download_link(value):
    dff = csvdownload[['Variable', value]]
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote_plus(csv_string)
    return csv_string


##TAB1 CALLBACKS

###Units and Vacancies Table
@app.callback(
    dash.dependencies.Output('units-vacancy', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_units_vacancy(value):
    units = data[data['NAME'] == value]
    units = units[['Vacant Housing Units', 'Homeowner Vacancy Rate', 'Rental Vacancy Rate', 'Homeownership Rate', 
    'Rental Rate']]
    units['Vacant Housing Units'] = units.apply(lambda x: "{:,}".format(round(x['Vacant Housing Units'])), axis=1)
    units['Homeowner Vacancy Rate'] = units.apply(lambda x: "{:.1%}".format(float(x['Homeowner Vacancy Rate'])), axis=1)
    units['Rental Vacancy Rate'] = units.apply(lambda x: "{:.1%}".format(float(x['Rental Vacancy Rate'])), axis=1)
    units['Homeownership Rate'] = units.apply(lambda x: "{:.1%}".format(float(x['Homeownership Rate'])), axis=1)
    units['Rental Rate'] = units.apply(lambda x: "{:.1%}".format(float(x['Rental Rate'])), axis=1)
    units = units.transpose()
    units.columns = [' ']
    dff_cols = ['Vacant Housing Units', 'Homeowner Vacancy Rate', 'Rental Vacancy Rate', 'Homeownership Rate', 
    'Rental Rate']
    units.insert(0,'Vacancy and Tenure Rates', dff_cols, True) 
    fig3 =  ff.create_table(units)
    fig3.layout.autosize == 'true'
    
    return fig3


###Unit Type Graph
@app.callback(
    dash.dependencies.Output('units-type', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_units_type(value):
    unit_type = data[data['NAME'] == value]
    unit_type = unit_type[['Single Family, Detached', 'Single Family, Attached', 'Duplex Units', 'Triplex or Fourplex','Low Rise Multifamily (5-9 units)',
    'Medium Rise Multifamily (10-19 units)', 'Large Multifamily (20+ units)','Mobile Home','Other (Boat, RV, van, etc.)']]
    unit_type = unit_type.transpose()
    unit_type.columns = ['# of Units']
    utype_list = ['Single Family, Detached', 'Single Family, Attached', 'Duplex Units', 'Triplex or Fourplex','Low Rise Multifamily (5-9 units)',
    'Medium Rise Multifamily (10-19 units)', 'Large Multifamily (20+ units)','Mobile Home','Other (Boat, RV, van, etc.)']
    unit_type.insert(0,'Unit Type', utype_list, True) 
    fig = px.bar(unit_type, x='Unit Type', y='# of Units', text = '# of Units')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside', cliponaxis = False)
    fig.layout.autosize == 'true'
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig.update_traces(marker_color='steelblue')
    return fig


###Num of Bedrooms Graph
@app.callback(
    dash.dependencies.Output('bed-t', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_beds(value):
    bed = data[data['NAME'] == value]
    bed = bed[['Studio Units', '1 Bedroom Units', '2 Bedroom Units', '3 Bedroom Units','4 Bedroom Units','5+ Bedroom Units']]
    bed = bed.transpose()
    bed.columns = ['# of Units']
    b_list = ['Studio Units', '1 Bedroom Units', '2 Bedroom Units', '3 Bedroom Units','4 Bedroom Units','5+ Bedroom Units']
    bed.insert(0,'# of Bedrooms', b_list, True) 
    fig13 = px.bar(bed, x='# of Bedrooms', y='# of Units', text='# of Units')
    fig13.update_traces(texttemplate='%{text:.2s}', textposition='outside', cliponaxis = False)
    fig13.layout.autosize == 'true'
    fig13.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig13.update_traces(marker_color='steelblue')
    return fig13

###Age of Units Graph
@app.callback(
    dash.dependencies.Output('unit-age', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_unit_age(value):
    unitage = data[data['NAME'] == value]
    unitage = unitage[['Units Built 1939 or Earlier','Units Built Between 1940 and 1949','Units Built Between 1950 and 1959',
    'Units Built Between 1960 and 1969','Units Built Between 1970 and 1979','Units Built Between 1980 and 1989','Units Built Between 1990 and 1999',
    'Units Built Between 2000 and 2009','Units Built 2010 and Later']]
    builtyear = ['Units Built 1939 or Earlier','Units Built Between 1940 and 1949','Units Built Between 1950 and 1959',
    'Units Built Between 1960 and 1969','Units Built Between 1970 and 1979','Units Built Between 1980 and 1989','Units Built Between 1990 and 1999',
    'Units Built Between 2000 and 2009','Units Built 2010 and Later']
    unitage = unitage.transpose()
    unitage.columns = ['# of Units']
    
    unitage.insert(0,'Year Built', builtyear, True)
    fig100 = px.bar(unitage, x='Year Built', y='# of Units', text = '# of Units')
    fig100.update_traces(texttemplate='%{text:.2s}', textposition='outside', cliponaxis = False)
    fig100.layout.autosize == 'true'
    fig100.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig100.update_traces(marker_color='steelblue')
    return fig100

###Assisted Households Table
@app.callback(
    dash.dependencies.Output('hud-units', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hudunits(value):
    if "Puerto Rico" not in value:
        h1 = data[data['NAME'] == value]

        h2= h1[['Project Based Section 8', 'Housing Choice Vouchers', 'Public Housing', '202/PRAC', '811/PRAC', 'Mod Rehab',
        'S236/BMIR', 'RentSup/RAP', 'LIHTC Units']]
        h2.columns = ['Public Housing Units', 'Houcing Choice Voucher Recipients', 'Mod Rehab Units', 'Project Based Voucher Units', 'RenSup/RAP Units',
           'S236/BMIR Units', '202/PRAC Units', '811/PRAC Units', 'LIHTC Units']
        h2 = h2.transpose()
        h2 = h2.reset_index()

        h2.columns = ['HUD Assisted Units/Households ', '']
        h2 = h2[h2[''] > 0]
        h2[''] = h2[''].apply(lambda x: "{:,}".format(round(x)))
        
        fig4 =  ff.create_table(h2)
        return fig4


    else:
        return no_data_fig

#TAB 2 CALLBACKS

##Income and Costs Table
@app.callback(
    dash.dependencies.Output('hh-inc', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hhinc(value):
    incomeandmediancosts = data[data['NAME'] == value]
    incomeandmediancosts = incomeandmediancosts[['Median Household Income', 'Median Home Value', 'Median Gross Rent', 
    'Median Monthly Owner Costs (Mortgage)','Median Monthly Owner Costs (No Mortgage)']]
    incomeandmediancosts['Median Monthly Household Income'] = float(incomeandmediancosts['Median Household Income']/12)
    incomeandmediancosts = incomeandmediancosts[['Median Household Income','Median Monthly Household Income','Median Home Value', 
    'Median Gross Rent', 'Median Monthly Owner Costs (Mortgage)','Median Monthly Owner Costs (No Mortgage)']]
    incomeandmediancosts = incomeandmediancosts.transpose()
    iccol = ['Median Household Income', 'Median Monthly Household Income', 'Median Home Value', 'Median Gross Rent', 'Median Monthly Owner Costs (Mortgage)',
        'Median Monthly Owner Costs (No Mortgage)']
    incomeandmediancosts .insert(0,'Median Monthly Household Income', iccol, True)  
    incomeandmediancosts .columns = ['Income and Housing Costs', '']
    m1 = list(incomeandmediancosts [''])
    m1 = [locale.currency(x, grouping=True ) for x in m1]
    incomeandmediancosts .insert(1,'m1', m1, True) 
    incomeandmediancosts  = incomeandmediancosts .drop('', axis=1)
    incomeandmediancosts .columns = ['Income and Housing Costs', '']

    ###Create Table
    fig7 = ff.create_table(incomeandmediancosts)
    return fig7


##Rent Gap Graph
@app.callback(
    dash.dependencies.Output('rent-gap', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'),
    dash.dependencies.Input('rentradio', 'value')])
def update_rentgap(value, radio):
    if "Puerto Rico" not in value:
        rentgap = data[data['NAME'] == value]
        if radio == 'grossgap':
            rentgap = rentgap[['grossless30rentgap','gross3050rentgap','gross5080rentgap','gross80uprentgap']]
        else:
            rentgap = rentgap[['netless30rentgap','net3050rentgap','net5080rentgap','net80uprentgap']]
        
        rentgap_col= ['Households Making Less than 30% AMI', 'Households Making Between 30% and 50% AMI', 
        'Households Making Between 50% and 80% AMI', 'Households Making More Than 80% AMI']
        rentgap.columns = rentgap_col
        rentgap = rentgap.transpose()
        rentgap.insert(0,'Household Income', rentgap_col, True)
        rentgap.columns = ['Household Income', 'Unit Surplus/Deficit']
        yaxis = rentgap['Unit Surplus/Deficit'].tolist()
        rentgap['color'] = np.where(rentgap['Unit Surplus/Deficit']<0,'indianred', 'steelblue')

        ###Create Figure
        fig5 = px.bar(rentgap, x='Household Income', y='Unit Surplus/Deficit')
        fig5.update_traces(marker_color=rentgap['color'])
        fig5.update_traces(texttemplate=yaxis,textposition='outside', cliponaxis = False)
        fig5.update_layout(title_text='Rental Gap Analysis')
        fig5.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
        return fig5
    else:
        return no_data_fig


##Home Gap Graph
@app.callback(
    dash.dependencies.Output('home-gap', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'),
    dash.dependencies.Input('homeradio', 'value')])
def update_homegap(value, radio):
    if "Puerto Rico" not in value:
        homegap = data[data['NAME'] == value]
        
        if radio == 'grossgap':
            homegap = homegap[['grossless50owngap','gross5080owngap','gross80100owngap','gross100upowngap']]
        else:
             homegap = homegap[['netless50owngap','net5080owngap','net80100owngap','net100upowngap']]

        homegap_col= ['Households Making Less than 50% AMI', 'Households Making Between 50% and 80% AMI', 
        'Households Making Between 80% and 100% AMI', 'Households Making More Than 100% AMI']
        homegap.columns = homegap_col
        homegap = homegap.transpose()
        homegap.insert(0,'Household Income', homegap_col, True) 
        homegap.columns = ['Household Income', 'Unit Surplus/Deficit']
        yaxis = homegap['Unit Surplus/Deficit'].tolist()
        homegap['color'] = np.where(homegap['Unit Surplus/Deficit']<0,'indianred', 'steelblue')
        ###Create Figure
        fig6 = px.bar(homegap, x='Household Income', y='Unit Surplus/Deficit')
        fig6.update_layout(title_text='Homeownership Gap Analysis')
        fig6.update_traces(marker_color=homegap['color'])
        fig6.update_traces(texttemplate=yaxis, textposition='outside', cliponaxis = False)
        fig6.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
        return fig6
    else:
        return no_data_fig

###Income & Costs Graph
@app.callback(
    dash.dependencies.Output('m-dist', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'),
    dash.dependencies.Input('mdropdown', 'value')])
def updatehcosts(value,tablechoice):
    worksheet= data[data['NAME'] == value]

    if tablechoice == 'Household Income':
        worksheet = worksheet[['HH Income Less than $10,000', 'HH Income $10,000 - $14,999', 'HH Income $15,000 - $24,999', 'HH Income $25,000 - $34,999', 
                      'HH Income $35,000 - $49,999', 'HH Income $50,000 - $74,999', 'HH Income $75,000 - $99,999', 'HH Income $100,000 - $149,999', 
                      'HH Income $150,000 - $199,999', 'HH Income $200,000 or More']]
        x_axis = ['Less than $10,000', '$10,000 - $14,999', '$15,000 - $24,999', '$25,000 - $34,999', '$35,000 - $49,999', '$50,000 - $74,999', '$75,000 - $99,999', '$100,000 - $149,999', 
                '$150,000 - $199,999', '$200,000 or More']
        y_axis = list(worksheet.iloc[0])
    elif tablechoice == 'Monthly Rent':
        worksheet = worksheet[['Rent Less than $500', 'Rent $500 - $999', 'Rent $1,000 - $1,499', 'Rent $1,500 - $1,999', 'Rent $2,000 - $2,499', 
                       'Rent $2,500 - $2,999', 'Rent $3,000 or More']]
        x_axis = ['Less than $500', '$500 - $999', '$1,000 - $1,499', '$1,500 - $1,999', '$2,000 - $2,499', '$2,500 - $2,999',
                '$3,000 or More']
        y_axis = list(worksheet.iloc[0])
    elif tablechoice == 'Monthly Homeowner Costs (Mortgage)':
        worksheet = worksheet[['Mortgage Less than $500', 'Mortgage $500 - $999', 'Mortgage $1,000 - $1,499', 'Mortgage $1,500 - $1,999', 
                       'Mortgage $2,000 - $2,499', 'Mortgage $2,500 - $2,999', 'Mortgage $3,000 or More']]
        x_axis = ['Less than $500', '$500 - $999', '$1,000 - $1,499', '$1,500 - $1,999', '$2,000 - $2,499', '$2,500 - $2,999',
                '$3,000 or More']
        y_axis = list(worksheet.iloc[0])
    else:
        worksheet = worksheet[['Homeowner Costs Less than $250', 'Homeowner Costs $250 - $399', 'Homeowner Costs $400 - $599', 
                         'Homeowner Costs $600 - $799', 'Homeowner Costs $800 - $999', 'Homeowner Costs $1,000 or More']]
        x_axis = ['Less than $250', '$250 - $399', '$400 - $599', '$600 - $799', '$800 - $999', '$1,000 or More']
        y_axis = list(worksheet.iloc[0])
    
    fig15 = go.Figure(data=[go.Bar(x=x_axis, y=y_axis)])
    fig15.update_layout(
        yaxis=dict(
        title='Count of Households',
        titlefont_size=16,),
    )
    fig15.update_traces(texttemplate=y_axis, textposition='outside', cliponaxis = False)
    fig15.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig15.update_traces(marker_color='steelblue')
    return fig15

##Household Assistance Table
@app.callback(
    dash.dependencies.Output('hh-assist', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hhassist(value):
    ###Pull Data
    assistance= data[data['NAME'] == value]
    assistance = assistance[['% of Households on Social Security','% of Households Receiving Retirement Income',
    '% of Households Receiving SSI','% of Households Receiving Cash Assistance','% of Households Receiving SNAP Benefits']]
   
    assistance['% of Households on Social Security'] = assistance.apply(lambda x: "{:.1%}".format(float(x['% of Households on Social Security'])), axis=1)
    assistance['% of Households Receiving Retirement Income'] = assistance.apply(lambda x: "{:.1%}".format(float(x['% of Households Receiving Retirement Income'])), axis=1)
    assistance['% of Households Receiving SSI'] = assistance.apply(lambda x: "{:.1%}".format(float(x['% of Households Receiving SSI'])), axis=1)
    assistance['% of Households Receiving Cash Assistance'] = assistance.apply(lambda x: "{:.1%}".format(float(x['% of Households Receiving Cash Assistance'])), axis=1)
    assistance['% of Households Receiving SNAP Benefits'] = assistance.apply(lambda x: "{:.1%}".format(float(x['% of Households Receiving SNAP Benefits'])), axis=1)
    assistance = assistance.transpose()
    assistance.columns = [' ']
    clab = ['% of Households on Social Security', '% of Households with Retirement Income' , '% of Households with SSI', 
        '% of Households Receiving Cash Assistance', '% of Households Receiving SNAP Benefits']
    assistance.insert(0,'Household Income and Assistance', clab, True) 
    
    ###Create Table
    fig8 = ff.create_table(assistance)
    return fig8


#TAB 3 CALLBACKS

##Historical Population Trend
@app.callback(
    dash.dependencies.Output('hist', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hist(value):
    if "Puerto Rico" not in value:
        ###Pull and Collate Data
        hist1 = hist[hist['map'] == value]
        current = data[data['NAME'] == value]
        current = current[['Total Population']]
        currentpop = current['Total Population'].iloc[0]
        hist1['current'] = currentpop
        yrs = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2015']
        yrs.append(str(year))
        hist2 = hist1.transpose()
        hist2 = hist2.iloc[3:]
        hist2.columns = ['Population']
        hist2.insert(0,'Year', yrs, True)

        ###Create Graph
        fig9 = go.Figure(data=go.Scatter(x=hist2['Year'], y=hist2['Population']))
        fig9.update_layout(title='Total Population over Time',
                    xaxis_title='Year',
                    yaxis_title='Population Count')
        fig9.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
        fig9.update_traces(line = dict(color = 'steelblue', width = 4), marker = dict(color = 'steelblue', size = 7))
        return fig9
    else:
        return no_data_fig

##Household Size
@app.callback(
    dash.dependencies.Output('hhsize', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hhsize(value):
    ###Pull and Collate Data
    hhs = data[data['NAME'] == value]
    hhs = hhs[['1 Person Households', '2 Person Households', '3 Person Households', '4+ Person Households']]
    hsize = ['1 Person Households', '2 Person Households', '3 Person Households', '4 + Person Households']
    hhs = hhs.transpose()
    hhs.columns = ['# of Households']
    hhs.insert(0, 'Household Size', hsize, True)
    y_axis = hhs['# of Households'].tolist()

    ###Create Graph
    fig14 = px.bar(hhs, x='Household Size', y='# of Households')
    fig14.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig14.update_traces(texttemplate=y_axis, textposition='outside', cliponaxis = False)
    fig14.update_traces(marker_color='steelblue')
    return fig14

##Population by Age
@app.callback(
    dash.dependencies.Output('age-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_ages(value):
    ###Pull and Collate Data
    popage = data[data['NAME'] == value]

    malelist = ['Male 0-4 years', 'Male 5-9 years','Male 10-14 years','Male 15-19 years',
               'Male 20-24 years','Male 25-29 years','Male 30-34 years','Male 35-44 years','Male 45-54 years',
               'Male 55-64 years','Male 65-74 years','Male 75-84 years','Male 85 years +']
    femalelist = ['Female 0-4 years', 'Female 5-9 years','Female 10-14 years','Female 15-19 years',
               'Female 20-24 years','Female 25-29 years','Female 30-34 years','Female 35-44 years','Female 45-54 years',
               'Female 55-64 years','Female 65-74 years','Female 75-84 years','Female 85 years +']
    
    females = popage[femalelist]
    females = females.iloc[0].tolist()
    males = popage[malelist]
    males = males.iloc[0].tolist()

    age = ['0-4 years', '5-9 years', '10-14 years', '15-19 years', '20-24 years', '25-29 years', '30-34 years', '35-44 years',
    '45-54 years', '55-64 years', '65-74 years', '75-84 years', '85 + years']

    female_pop = females
    male_pop = males
    age1 = age
    
    ###Create Graph
    fig10 = make_subplots(shared_xaxes=False,
                    shared_yaxes=True, vertical_spacing=0.001)
    fig10.append_trace(go.Bar(
        x=female_pop,
        y=age,
        marker=dict(
            color='grey',
        ),
        name='Female Population',
        orientation='h',
    ), 1, 1)
    fig10.append_trace(go.Bar(
        x=male_pop,
        y=age1,
        marker=dict(
            color='steelblue',
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
    fig10.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig10.update_xaxes(nticks=10)   
    return fig10


##Population by Race
@app.callback(
    dash.dependencies.Output('race-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_race(value):
    ###Pull and Collate Data
    race = data[data['NAME'] == value]
    race = race[['White', 'Black', 'Latinx', 'Native American/Alaskan Native', 'Asian', 'Hawaiian/Pacific Islander', 'Other Race',
    'Two or More Races']]
    racelist = ['White', 'Black', 'Latinx', 'Native American/Alaskan Native', 'Asian', 'Hawaiian/Pacific Islander', 'Other Race',
    'Two or More Races']
    race = race.transpose()
    race.columns = ['Population Count']
    race.insert(0,'Population by Race', racelist, True)
    y_axis = race['Population Count'].tolist()
    
    ###Create Graph
    fig25 = px.bar(race, x='Population by Race', y='Population Count')
    fig25.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig25.update_traces(texttemplate=y_axis, textposition='outside', cliponaxis = False)
    fig25.update_traces(marker_color='steelblue')
    return fig25


##Population by Sex
@app.callback(
    dash.dependencies.Output('sex-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_sex(value):
    ###Pull and Collate Data
    sex = data[data['NAME'] == value]
    sex = sex[['Male Population', 'Female Population']]
    sexlist = ['Male', 'Female']
    sex = sex.transpose()
    sex.columns = ['Population Count']
    sex.insert(0,'Population by Sex', sexlist, True) 

    ###Create Graph
    fig12 = px.bar(sex, x='Population by Sex', y='Population Count')
    fig12.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fi12.update_traces(marker_color='steelblue')
    return fig12

##Special Populations Table
@app.callback(
    dash.dependencies.Output('spec-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_special(value):
    ###Pull and Collate Data
    special = data[data['NAME'] == value]
    special = special[['% of Single Parent Househods','% of Inidividuals with a Disability','% of Inidividuals 65 or Older with a Disability',
    '% of Non-Fluent English Speakers']]

    special['% of Single Parent Househods'] = special.apply(lambda x: "{:.1%}".format(x['% of Single Parent Househods']), axis=1)
    special['% of Inidividuals with a Disability'] = special.apply(lambda x: "{:.1%}".format(x['% of Inidividuals with a Disability']), axis=1)
    special['% of Inidividuals 65 or Older with a Disability'] = special.apply(lambda x: "{:.1%}".format(x['% of Inidividuals 65 or Older with a Disability']), axis=1)
    special['% of Non-Fluent English Speakers'] = special.apply(lambda x: "{:.1%}".format(x['% of Non-Fluent English Speakers']), axis=1)
    special = special.transpose()
    hhs = ['% of Single Parent Households', '% of People with a Disability', '% of Individuals 65 and Over with a Disability', '% of Non-Fluent English Speakers']
    special.columns = [' ']
    special.insert(0,'Special Populations', hhs, True) 


    ###Create Table
    fig12 = ff.create_table(special)
    return fig12

if __name__ == '__main__':
    app.run_server(debug=True)
