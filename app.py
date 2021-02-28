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
df = pd.read_csv(str(census_path /"DP04acs5_county.csv"))
dp = pd.read_csv(str(census_path / "DP02acs5_county.csv"))
ep = pd.read_csv(str(census_path / "DP03acs5_county.csv"))
tp = pd.read_csv(str(census_path / "DP05acs5_county.csv"))

df_cols = df.columns.values
df_cols[0] = 'County Name'
df.columns = df_cols

dp_cols = dp.columns.values
dp_cols[0] = 'County Name'
dp.columns = dp_cols

ep_cols = ep.columns.values
ep_cols[0] = 'County Name'
ep.columns = ep_cols

tp_cols = tp.columns.values
tp_cols[0] = 'County Name'
tp.columns = tp_cols

low_memory = False

#HUD Program and LIHTC Data
hud1 = pd.read_csv(str(hud_path / "hudunits.csv"))
litc = pd.read_csv(str(hud_path / "lihtc.csv"))

#HUD CHAS and Household Size Data
sevena = pd.read_csv(str(chas_path / "Table17A.csv"), encoding='cp1252')
sevenb = pd.read_csv(str(chas_path / "Table17B.csv"), encoding='cp1252')
eighta = pd.read_csv(str(chas_path / "Table18A.csv"), encoding='cp1252')
eightb = pd.read_csv(str(chas_path / "Table18B.csv"), encoding='cp1252')
eightc = pd.read_csv(str(chas_path / "Table18C.csv"), encoding='cp1252')
hhs = pd.read_csv(str(census_path / "acs5_s2501.csv"))

#Historical Pop Data
hist = pd.read_csv(str(pop_path / "h_pop.csv"))

#Option Lists
monthly_options = ['Household Income', 'Monthly Rent', 'Monthly Homeowner Costs (Mortgage)', 'Monthly Homeowner Costs (No Mortgage)']

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
    html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Housing Inventory', value='tab-1'),
        dcc.Tab(label='Housing Affordability', value='tab-2'),
        dcc.Tab(label = 'Housing Demand', value = 'tab-3')
    ]),
    html.Div(id='tabs-example-content')
    ]),
    html.Div(
    className="app-footer",
    children=[
        html.Div('Housing Profile Dashboard v1.3: Produced By Devin McNally and Ryan McNally', className="app-footer--text"),
        html.Div('All data is collected and presented at no cost. If you use this, please attribute this project!', className="app-footer--text"),
        html.Div('Last Updated: February 6, 2021', className="app-footer--text")
        ]
    ),
])



#CALLBACKS
    
##Tab Control    
@app.callback(
    dash.dependencies.Output('tabs-example-content', 'children'),
    [dash.dependencies.Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(
                ' ',
                className = 'body-break'
            ),
            html.Div(className = 'main',
                children = [
                html.Div(
                    className = 'main-cards',
                    children = [
                    html.Div(
                        className = 'box',
                        children = [  
                            html.Div([
                                dcc.Graph(id = 'units-vacancy'),
                            ]),
                        ]    
                    ),
                    html.Div(
                        className = 'box',
                        children = [
                            html.Div([
                                dcc.Graph(id = 'units-type'),
                            ]),    
                        ]
                    ), 
                    html.Div(
                        className = 'box',
                        children = [
                            html.Div([
                                dcc.Graph(id = 'bed-t'),
                            ]),
                        ]
                    ),
                    html.Div(
                        className = 'box',
                        children = [
                            html.Div([
                                dcc.Graph(id = 'unit-age'),
                            ]),
                        ]
                    ),
                    html.Div(
                        className = 'box',
                        children = [
                            html.Div([
                                dcc.Graph(id = 'hud-units'),
                            ]),
                        ]
                    ),           
                    html.Div(
                        className = 'box',
                        children = [
                            html.Div([
                                html.H4('Sources:'),
                                html.H6('1) U.S. Census Bureau, American Community Survey Table: DP04, latest 5-Year Estimates'),
                                html.H6('2) U.S. Census Bureau, American Community Survey Table: DP04, latest 5-Year Estimates'),
                                html.H6('3) U.S. Census Bureau, American Community Survey Table: DP04, latest 5-Year Estimates'),
                                html.H6('4) U.S. Census Bureau, American Community Survey Table: DP04, latest 5-Year Estimates'),
                                html.H6('5) HUD Picture of Subsidized Households & Low-Income Housing Tax Credit Data Dataset, 2019')
                            ]),
                        ]
                    )           
                    ]
                ),
            ]),
        ]
        )        

    elif tab == 'tab-2':
        return html.Div([
            html.Div(
                ' ',
                className = 'body-break'
            ),
            html.Div(
                className = 'row two columns',
                children = [
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'hh-inc'),
                        ]),
                    ]    
                ),
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'hh-assist'),
                        ]),
                    ]    
                ),
            ]),
            html.Div(
                className = 'row two columns',
                children = [
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'rent-gap'),
                        ]),
                    ]    
                ),
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'home-gap'),
                        ]),
                    ]    
                ),
            ]),
            html.Div(
                className = 'row two columns',
                children = [
                html.Div(
                    className = 'box',
                    children = [
                        html.Div(
                            dcc.Dropdown(
                            id='mdropdown',
                            options=[{"label":c, "value":c} for c in sorted(monthly_options)],
                            placeholder = 'Household Income',
                            value = 'Household Income'),
                            className = 'regulardd'),
                        html.Div([
                            dcc.Graph(id = 'm-dist'),
                        ]),
                    ]    
                ),
            ]),
            html.Div(
                className = 'row two columns',
                children = [ 
                html.Div(
                    className = 'box',
                    children = [
                        html.Div([
                            html.H4('Sources:'),
                            html.H6('1) U.S. Census Bureau, American Community Survey Table: DP03 & DP04, latest 5-Year Estimates'),
                            html.H6('2) U.S. Census Bureau, American Community Survey Table: DP03, latest 5-Year Estimates'),
                            html.H6('3) HUD CHAS Dataset, 2012-2016'),
                            html.H6('4) HUD CHAS Dataset, 2012-2016'),
                            html.H6('5) U.S. Census Bureau, American Community Survey Table: DP03 & DP04, latest 5-Year Estimates')
                        ]),
                    ]
                )           
                ]
            ),
        ])

    elif tab == 'tab-3':
        return html.Div([
            html.Div(
                ' ',
                className = 'body-break'
            ),
            html.Div(
                className = 'row two columns',
                children = [
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'hist'),
                        ]),
                    ]    
                ),
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'hhsize'),
                        ]),
                    ]    
                ),
            ]),
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
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'race-g'),
                        ]),
                    ]    
                ),
            ]),
            html.Div(
                className = 'row two columns',
                children = [
                html.Div(
                    className = 'box',
                    children = [  
                        html.Div([
                            dcc.Graph(id = 'spec-g'),
                        ]),
                    ]    
                ),
            ]),
            html.Div(
                className = 'row two columns',
                children = [ 
                html.Div(
                    className = 'box',
                    children = [
                        html.Div([
                            html.H4('Sources:'),
                            html.H6('1) Source: U.S. Census Bureau, Population of States and Counties of the United States: 1790 to 1990, Decennial Census SF1: 2000, ACS 2015 5-Year Estimates'),
                            html.H6('2) U.S. Census Bureau, American Community Survey Table: S2501, latest 5-Year Estimates'),
                            html.H6('3) U.S. Census Bureau, American Community Survey Table: DP05, latest 5-Year Estimates'),
                            html.H6('4) U.S. Census Bureau, American Community Survey Table: DP05, latest 5-Year Estimates'),
                            html.H6('5) U.S. Census Bureau, American Community Survey Table: DP05, latest 5-Year Estimates'),
                        ]),
                    ]
                )           
                ]
            ),
        ])


##County Proflie Name Control
@app.callback(
    dash.dependencies.Output('county-name', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def countyn_update(value):
    return 'Housing Profile: {}'.format(value)

##TAB1 CALLBACKS

###Units and Vacancies Table
@app.callback(
    dash.dependencies.Output('units-vacancy', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_units_vacancy(value):
    dff = df[df['County Name'] == value]
    dff = dff[['DP04_0001E','DP04_0003E','DP04_0004E','DP04_0005E','DP04_0046E','DP04_0047E']]
    dff['DP04_0004E'] = dff['DP04_0004E']/100
    dff['DP04_0005E'] = dff['DP04_0005E']/100
    dff['DP04_0046E'] = dff['DP04_0046E']/(dff['DP04_0046E'] + dff['DP04_0047E']) 
    dff['DP04_0047E'] = 1 - dff['DP04_0046E']
    dff['DP04_0001E'] = round( dff['DP04_0001E'])
    dff['DP04_0001E'] = dff.apply(lambda x: "{:,}".format(x['DP04_0001E']), axis=1)
    dff['DP04_0003E'] = dff.apply(lambda x: "{:,}".format(x['DP04_0003E']), axis=1)
    dff['DP04_0004E'] = dff.apply(lambda x: "{:.1%}".format(float(x['DP04_0004E'])), axis=1)
    dff['DP04_0005E'] = dff.apply(lambda x: "{:.1%}".format(float(x['DP04_0005E'])), axis=1)
    dff['DP04_0046E'] = dff.apply(lambda x: "{:.1%}".format(float(x['DP04_0046E'])), axis=1)
    dff['DP04_0047E'] = dff.apply(lambda x: "{:.1%}".format(float(x['DP04_0047E'])), axis=1)
    dff = dff.transpose()
    dff.columns = [' ']
    dff_cols = ['Total Housing Units', 'Vacant Housing Units', 'Homeowner Vacancy Rate', 'Rental Vacancy Rate', 'Homeowner Share of Households', 
    'Renter Share of Households']
    dff.insert(0,'Total Units and Vacancies', dff_cols, True) 
    fig3 =  ff.create_table(dff)
    
    return fig3


###Unit Type Graph
@app.callback(
    dash.dependencies.Output('units-type', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_units_type(value):
    dfg = df[df['County Name'] == value]
    dfg = dfg[['DP04_0007E','DP04_0008E','DP04_0009E','DP04_0010E','DP04_0011E','DP04_0012E','DP04_0013E','DP04_0014E','DP04_0015E']]
    dfg = dfg.transpose()
    dfg.columns = ['# of Units']
    htype_list = ['Single Family, Detached', 'Single Family, Attached', 'Duplex Units', 'Triplex or Fourplex','Low Rise Multifamily (5-9 units)','Medium Rise Multifamily (10-19 units)',
            'Large Multifamily (20+ units)','Mobile Home','Other (Boat, RV, van, etc.)'
            ]
    dfg.insert(0,'Unit Type', htype_list, True) 
    fig = px.bar(dfg, x='Unit Type', y='# of Units')

    return fig


###Num of Bedrooms Graph
@app.callback(
    dash.dependencies.Output('bed-t', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_beds(value):
    bed = df[df['County Name'] == value]
    bed1 = bed[['DP04_0039E', 'DP04_0040E', 'DP04_0041E', 'DP04_0042E', 'DP04_0043E', 'DP04_0044E']]
    bed2 = bed1.transpose()
    bed2.columns = ['# of Units']
    b_list = ['Studio Units', '1 Bedroom Units', '2 Bedroom Units', '3 Bedroom Units','4 Bedroom Units','5+ Bedroom Units']
    bed2.insert(0,'# of Bedrooms', b_list, True) 
    fig13 = px.bar(bed2, x='# of Bedrooms', y='# of Units')
    
    return fig13

###Age of Units Graph
@app.callback(
    dash.dependencies.Output('unit-age', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_unit_age(value):
    df3 = df[df['County Name'] == value]
    df3 = df3[['DP04_0016E','DP04_0019E','DP04_0020E', 'DP04_0021E','DP04_0022E', 'DP04_0023E', 
          'DP04_0024E', 'DP04_0025E','DP04_0026E']]
    df3['Units Built Before 2010'] = (df3['DP04_0019E'] + 
                                    df3['DP04_0020E'] + 
                                    df3['DP04_0021E'] + 
                                    df3['DP04_0022E'] + 
                                    df3['DP04_0023E'] + 
                                    df3['DP04_0024E'] + 
                                    df3['DP04_0025E'] + 
                                    df3['DP04_0026E'])
    df3['Units Built 2010 and Later'] = df3['DP04_0016E'] - df3['Units Built Before 2010']
    
    df3 = df3[['DP04_0026E','DP04_0025E', 'DP04_0024E','DP04_0023E', 'DP04_0022E', 
          'DP04_0021E', 'DP04_0020E','DP04_0019E','Units Built 2010 and Later']]
    builtyear = ['Units Built 1939 or Earlier', 'Units Built Between 1940 and 1949', 'Units Built Between 1950 and 1959', 'Units Built Between 1960 and 1969', 'Units Built Between 1970 and 1979',
'Units Built Between 1980 and 1989', 'Units Built Between 1990 and 1999', 'Units Built Between 2000 and 2009', 'Units Built 2010 and Later']
    df3 = df3.transpose()
    df3.columns = ['# of Units']
    
    df3.insert(0,'Year Built', builtyear, True)
    fig100 = px.bar(df3, x='Year Built', y='# of Units')
    return fig100

###Assisted Households Table
@app.callback(
    dash.dependencies.Output('hud-units', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hudunits(value):
    if "Puerto Rico" not in value:
        h1 = hud1[hud1['location'] == value]
        h2= h1[['program_label', 'number_reported']]
        h2.columns = ['HUD Program', '# of Household Recipients']
        h3 = h2[h2['# of Household Recipients'] > 0]
        l1 = litc[litc['location'] == value]
        l2 = l1[l1['li_units'].notnull()]
        li_u = l2['li_units'].sum()
        li_u = li_u.astype(int)
        prog = h3['HUD Program'].tolist()
        prog.append('LIHTC')
        prognum = list(h3['# of Household Recipients'].values)
        prognum.append(li_u)
        progc = list(zip(prog,prognum))
        pt = pd.DataFrame(progc, columns=['HUD Program', '# of Household Recipients'])
        pt1 = pt[pt['# of Household Recipients'] > 0]
        if int(len(pt1['# of Household Recipients'])) > 1:
            pt1['# of Household Recipients'] = pt1.apply(lambda x: "{:,}".format(int(x['# of Household Recipients'])), axis=1)
            fig4 =  ff.create_table(pt1)
            return fig4
        else:
            return no_data_fig

    else:
        return no_data_fig

#TAB 2 CALLBACKS

##Income and Costs Table
@app.callback(
    dash.dependencies.Output('hh-inc', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hhinc(value):
    ###Pull Data
    ep1 = ep[ep['County Name'] == value]
    ep2 = ep1[['DP03_0062E']]
    ep3 = ep2['DP03_0062E']
    ep3 = float(ep3)
    hrv = df[df['County Name'] == value]
    hrv1 = hrv[['DP04_0089E','DP04_0134E','DP04_0101E','DP04_0109E']]

    ###Put Together Data
    hrv1.insert(0,'Median Household Income', ep3, True) 
    mo_inc = float(hrv1['Median Household Income']/12)
    hrv1.insert(1,'Median Monthly Household Income', mo_inc, True)
    hrv1 = hrv1.transpose()
    iccol = ['Median Household Income', 'Median Monthly Household Income', 'Median Home Value', 'Median Gross Rent', 'Median Monthly Owner Costs (Mortgage)',
        'Median Monthly Owner Costs (No Mortgage)']
    hrv1.insert(0,'Median Monthly Household Income', iccol, True)  
    hrv1.columns = ['Income and Housing Costs', '']
    m1 = list(hrv1[''])
    m1 = [locale.currency(x, grouping=True ) for x in m1]
    hrv1.insert(1,'m1', m1, True) 
    hrv1 = hrv1.drop('', axis=1)
    hrv1.columns = ['Income and Housing Costs', '']

    ###Create Table
    fig7 = ff.create_table(hrv1)
    return fig7


##Rent Gap Graph
@app.callback(
    dash.dependencies.Output('rent-gap', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_rentgap(value):
    if "Puerto Rico" not in value:
        ### Filter Tables
        # seva = sevena[sevena['name'] == value]
        sevb = sevenb[sevenb['name'] == value]
        # eia = eighta[eighta['name'] == value]
        # eib = eightb[eightb['name'] == value]
        eic = eightc[eightc['name'] == value]

        ### Pull Out Data and Create Variables
        renters_less30 = list(eic['T18C_est4']+eic['T18C_est10']+eic['T18C_est16']+eic['T18C_est22']+eic['T18C_est29']+eic['T18C_est35']+eic['T18C_est41']+eic['T18C_est47']+eic['T18C_est54']+eic['T18C_est60']+eic['T18C_est66']+eic['T18C_est72']+ eic['T18C_est79']+ eic['T18C_est85']+ eic['T18C_est91']+ eic['T18C_est97'])
        runits_less30 = list(eic['T18C_est3']+eic['T18C_est28']+eic['T18C_est53']+eic['T18C_est78'])
        vacant_less30 = list(sevb['T17B_est3']+sevb['T17B_est8']+sevb['T17B_est13']+sevb['T17B_est18'])
        # occabv_less30 = list(eic['T18C_est5']+eic['T18C_est6']+eic['T18C_est7']+eic['T18C_est8']+eic['T18C_est30']+eic['T18C_est31']+eic['T18C_est32']+eic['T18C_est33']+eic['T18C_est55']+eic['T18C_est56']+eic['T18C_est57']+eic['T18C_est58']+eic['T18C_est80']+eic['T18C_est81']+eic['T18C_est82']+eic['T18C_est83'])
        r_less30 = renters_less30[0]
        ru_less30 = runits_less30[0]
        v_less30 = vacant_less30[0]
        # ocabv_less30 = occabv_less30[0]
        rtu_less30 = ru_less30 + v_less30
        # prct_ocabv_less30 = float(ocabv_less30/rtu_less30)
        gap_less30 = rtu_less30 - r_less30
        # adj_gap_less30 = gap_less30 - ocabv_less30
        renters_30t50 = list(eic['T18C_est5']+eic['T18C_est11']+eic['T18C_est17']+eic['T18C_est23']+eic['T18C_est30']+eic['T18C_est36']+eic['T18C_est42']+eic['T18C_est48']+eic['T18C_est55']+eic['T18C_est61']+eic['T18C_est67']+eic['T18C_est73']+ eic['T18C_est80']+ eic['T18C_est86']+ eic['T18C_est92']+ eic['T18C_est98'])
        runits_30t50 = list(eic['T18C_est9']+eic['T18C_est34']+eic['T18C_est59']+eic['T18C_est84'])
        vacant_30t50 = list(sevb['T17B_est4']+sevb['T17B_est9']+sevb['T17B_est14']+sevb['T17B_est19'])
        # occabv_30t50 = list(eic['T18C_est12']+eic['T18C_est13']+eic['T18C_est14']+eic['T18C_est37']+eic['T18C_est38']+eic['T18C_est39']+eic['T18C_est62']+eic['T18C_est63']+eic['T18C_est64']+eic['T18C_est87']+eic['T18C_est88']+eic['T18C_est89'])
        r_30t50 = renters_30t50[0]
        ru_30t50 = runits_30t50[0]
        v_30t50 = vacant_30t50[0]
        # ocabv_30t50 = occabv_30t50[0]
        rtu_30t50 = ru_30t50 + v_30t50
        # prct_ocabv_30t50 = float(ocabv_30t50/rtu_30t50)
        gap_30t50 = rtu_30t50 - r_30t50
        # adj_gap_30t50 = gap_30t50 - ocabv_30t50
        renters_50t80 = list(eic['T18C_est6']+eic['T18C_est12']+eic['T18C_est18']+eic['T18C_est24']+eic['T18C_est31']+eic['T18C_est37']+eic['T18C_est43']+eic['T18C_est49']+eic['T18C_est56']+eic['T18C_est62']+eic['T18C_est68']+eic['T18C_est74']+ eic['T18C_est81']+ eic['T18C_est87']+ eic['T18C_est93']+ eic['T18C_est99'])
        runits_50t80 = list(eic['T18C_est15']+eic['T18C_est40']+eic['T18C_est65']+eic['T18C_est90'])
        vacant_50t80 = list(sevb['T17B_est5']+sevb['T17B_est10']+sevb['T17B_est15']+sevb['T17B_est20'])
        # occabv_50t80 = list(eic['T18C_est19']+eic['T18C_est20']+eic['T18C_est44']+eic['T18C_est45']+eic['T18C_est69']+eic['T18C_est70']+eic['T18C_est94']+eic['T18C_est95'])
        r_50t80 = renters_50t80[0]
        ru_50t80 = runits_50t80[0]
        v_50t80 = vacant_50t80[0]
        # ocabv_50t80 = occabv_50t80[0]
        rtu_50t80 = ru_50t80 + v_50t80
        # prct_ocabv_50t80 = float(ocabv_50t80/rtu_50t80)
        gap_50t80 = rtu_50t80 - r_50t80
        # adj_gap_50t80 = gap_50t80 - ocabv_50t80


        ###Create Dataframe
        rentgap_var = ['Households Making Less than 30% AMI', 'Households Making Between 30% and 50% AMI', 'Households Making Between 50% and 80% AMI']
        rentgap = [gap_less30, gap_30t50, gap_50t80]
        rgap1 = list(zip(rentgap_var,rentgap))
        rgap = pd.DataFrame(rgap1, columns=['Household Income', 'Unit Surplus/Deficit'])

        ###Create Figure
        fig5 = px.bar(rgap, x='Household Income', y='Unit Surplus/Deficit')
        fig5.update_layout(title_text='Rental Gap Analysis')
        return fig5
    else:
        return no_data_fig


##Home Gap Graph
@app.callback(
    dash.dependencies.Output('home-gap', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_homegap(value):
    if "Puerto Rico" not in value:
        ###Filter Tables
        seva = sevena[sevena['name'] == value]
        # sevb = sevenb[sevenb['name'] == value]
        eia = eighta[eighta['name'] == value]
        eib = eightb[eightb['name'] == value]
        # eic = eightc[eightc['name'] == value]

        ###Pull Out Data and Create Variables
        homem_less50 = list(eia['T18A_est4']+eia['T18A_est5']+eia['T18A_est10']+eia['T18A_est11']+eia['T18A_est16']+eia['T18A_est17']+eia['T18A_est22']+eia['T18A_est23']+eia['T18A_est29']+eia['T18A_est30']+eia['T18A_est35']+eia['T18A_est36']+eia['T18A_est41']+eia['T18A_est42']+eia['T18A_est47']+eia['T18A_est48']+eia['T18A_est54']+eia['T18A_est55']+eia['T18A_est60']+eia['T18A_est61']+eia['T18A_est66']+eia['T18A_est67']+eia['T18A_est72']+eia['T18A_est73']+eia['T18A_est79']+eia['T18A_est80']+eia['T18A_est85']+eia['T18A_est86']+eia['T18A_est91']+eia['T18A_est92']+eia['T18A_est97']+eia['T18A_est98'])
        homenom_less50 = list(eib['T18B_est4']+eib['T18B_est5']+eib['T18B_est10']+eib['T18B_est11']+eib['T18B_est16']+eib['T18B_est17']+eib['T18B_est22']+eib['T18B_est23']+eib['T18B_est29']+eib['T18B_est30']+eib['T18B_est35']+eib['T18B_est36']+eib['T18B_est41']+eib['T18B_est42']+eib['T18B_est47']+eib['T18B_est48']+eib['T18B_est54']+eib['T18B_est55']+eib['T18B_est60']+eib['T18B_est61']+eib['T18B_est66']+eib['T18B_est67']+eib['T18B_est72']+eib['T18B_est73']+eib['T18B_est79']+eib['T18B_est80']+eib['T18B_est85']+eib['T18B_est86']+eib['T18B_est91']+eib['T18B_est92']+eib['T18B_est97']+eib['T18B_est98'])
        hunits_less50 = list(eib['T18B_est3']+eib['T18B_est28']+eib['T18B_est53']+eib['T18B_est78']+eia['T18A_est3']+eia['T18A_est28']+eia['T18A_est53']+eia['T18A_est78'])
        hvac_less50 = list(seva['T17A_est3']+seva['T17A_est8']+seva['T17A_est13']+seva['T17A_est18'])
        # hoabvm_less50 = list(eia['T18A_est6']+eia['T18A_est7']+eia['T18A_est8']+eia['T18A_est31']+eia['T18A_est32']+eia['T18A_est33']+eia['T18A_est56']+eia['T18A_est57']+eia['T18A_est58']+eia['T18A_est81']+eia['T18A_est82']+eia['T18A_est83'])
        # hoabvnom_less50 = list(eib['T18B_est6']+eib['T18B_est7']+eib['T18B_est8']+eib['T18B_est31']+eib['T18B_est32']+eib['T18B_est33']+eib['T18B_est56']+eib['T18B_est57']+eib['T18B_est58']+eib['T18B_est81']+eib['T18B_est82']+eib['T18B_est83'])
        h_less50 = homem_less50[0] + homenom_less50[0]
        hu_less50 = hunits_less50[0]
        hv_less50 = hvac_less50[0]
        # habv_less50 = hoabvm_less50[0] + hoabvnom_less50[0]
        htu_less50 = hu_less50 + hv_less50
        # prct_habv_less50 = float(habv_less50/htu_less50)
        hgap_less50 = htu_less50 - h_less50
        # adj_hgap_less50 = hgap_less50 + habv_less50
        homem_50t80 = list(eia['T18A_est6']+eia['T18A_est12']+eia['T18A_est18']+eia['T18A_est24']+eia['T18A_est31']+eia['T18A_est37']+eia['T18A_est43']+eia['T18A_est49']+eia['T18A_est56']+eia['T18A_est62']+eia['T18A_est68']+eia['T18A_est74']+eia['T18A_est81']+eia['T18A_est87']+eia['T18A_est93']+eia['T18A_est99'])
        homenom_50t80 = list(eib['T18B_est6']+eib['T18B_est12']+eib['T18B_est18']+eib['T18B_est24']+eib['T18B_est31']+eib['T18B_est37']+eib['T18B_est43']+eib['T18B_est49']+eib['T18B_est56']+eib['T18B_est62']+eib['T18B_est68']+eib['T18B_est74']+eib['T18B_est81']+eib['T18B_est87']+eib['T18B_est93']+eib['T18B_est99'])
        hunits_50t80 = list(eib['T18B_est9']+eib['T18B_est34']+eib['T18B_est59']+eib['T18B_est84']+eia['T18A_est9']+eia['T18A_est34']+eia['T18A_est59']+eia['T18A_est84'])
        hvac_50t80 = list(seva['T17A_est4']+seva['T17A_est9']+seva['T17A_est14']+seva['T17A_est19'])
        # hoabvm_50t80 = list(eia['T18A_est13']+eia['T18A_est14']+eia['T18A_est38']+eia['T18A_est39']+eia['T18A_est63']+eia['T18A_est64']+eia['T18A_est88']+eia['T18A_est89'])
        # hoabvnom_50t80 = list(eib['T18B_est13']+eib['T18B_est14']+eib['T18B_est38']+eib['T18B_est39']+eib['T18B_est63']+eib['T18B_est64']+eib['T18B_est88']+eib['T18B_est89'])
        h_50t80 = homem_50t80[0] + homenom_50t80[0]
        hu_50t80 = hunits_50t80[0]
        hv_50t80 = hvac_50t80[0]
        # habv_50t80 = hoabvm_50t80[0] + hoabvnom_50t80[0]
        htu_50t80 = hu_50t80 + hv_50t80
        # prct_habv_50t80 = float(habv_50t80/htu_50t80)
        hgap_50t80 = htu_50t80 - h_50t80
        # adj_hgap_50t80 = hgap_50t80 + habv_50t80
        homem_80t100 = list(eia['T18A_est7']+eia['T18A_est13']+eia['T18A_est19']+eia['T18A_est25']+eia['T18A_est32']+eia['T18A_est38']+eia['T18A_est44']+eia['T18A_est50']+eia['T18A_est57']+eia['T18A_est63']+eia['T18A_est69']+eia['T18A_est75']+eia['T18A_est82']+eia['T18A_est88']+eia['T18A_est94']+eia['T18A_est100'])
        homenom_80t100 = list(eib['T18B_est7']+eib['T18B_est13']+eib['T18B_est19']+eib['T18B_est25']+eib['T18B_est32']+eib['T18B_est38']+eib['T18B_est44']+eib['T18B_est50']+eib['T18B_est57']+eib['T18B_est63']+eib['T18B_est69']+eib['T18B_est75']+eib['T18B_est82']+eib['T18B_est88']+eib['T18B_est94']+eib['T18B_est100'])
        hunits_80t100 = list(eib['T18B_est15']+eib['T18B_est40']+eib['T18B_est65']+eib['T18B_est90']+eia['T18A_est15']+eia['T18A_est40']+eia['T18A_est65']+eia['T18A_est90'])
        hvac_80t100 = list(seva['T17A_est5']+seva['T17A_est10']+seva['T17A_est15']+seva['T17A_est20'])
        # hoabvm_80t100 = list(eia['T18A_est20']+eia['T18A_est45']+eia['T18A_est70']+eia['T18A_est95'])
        # hoabvnom_80t100 = list(eib['T18B_est20']+eib['T18B_est45']+eib['T18B_est70']+eib['T18B_est95'])
        h_80t100 = homem_80t100[0] + homenom_80t100[0]
        hu_80t100 = hunits_80t100[0]
        hv_80t100 = hvac_80t100[0]
        # habv_80t100 = hoabvm_80t100[0] + hoabvnom_80t100[0]
        htu_80t100 = hu_80t100 + hv_80t100
        # prct_habv_80t100 = float(habv_80t100/htu_80t100)
        hgap_80t100 = htu_80t100 - h_80t100
        # adj_hgap_80t100 = hgap_80t100 + habv_80t100

        ###Create Dataframe
        homegap_var = ['Households Making Less than 50% AMI', 'Households Making Between 50% and 80% AMI', 'Households Making Between 80% and 100% AMI']
        homegap = [hgap_less50, hgap_50t80, hgap_80t100]
        hgap1 = list(zip(homegap_var,homegap))
        hgap = pd.DataFrame(hgap1, columns=['Household Income', 'Unit Surplus/Deficit'])
        
        
        ###Create Figure
        fig6 = px.bar(hgap, x='Household Income', y='Unit Surplus/Deficit')
        fig6.update_layout(title_text='Homeownership Gap Analysis')
        return fig6
    else:
        return no_data_fig

###Income & Costs Graph
@app.callback(
    dash.dependencies.Output('m-dist', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'),
    dash.dependencies.Input('mdropdown', 'value')])
def updatehcosts(value,tablechoice):
    rent_variables = ['DP04_0127E', 'DP04_0128E', 'DP04_0129E','DP04_0130E', 'DP04_0131E', 'DP04_0132E','DP04_0133E']
    homeownermort_variables = ['DP04_0094E','DP04_0095E','DP04_0096E','DP04_0097E','DP04_0098E','DP04_0099E','DP04_0100E']
    homeownernomort_variables = ['DP04_0103E','DP04_0104E','DP04_0105E','DP04_0106E','DP04_0107E','DP04_0108E']
    householdincome_variables = ['DP03_0052E','DP03_0053E','DP03_0054E','DP03_0055E','DP03_0056E','DP03_0057E','DP03_0058E','DP03_0059E',
                                'DP03_0060E','DP03_0061E']

    if tablechoice == 'Household Income':
        worksheet = ep[ep['County Name'] == value]
        worksheet = worksheet[householdincome_variables]
        x_axis = ['Less than $10,000', '$10,000 - $14,999', '$15,000 - $24,999', '$25,000 - $34,999', '$35,000 - $49,999', '$50,000 - $74,999', '$75,000 - $99,999', '$100,000 - $149,999', 
                '$150,000 - $199,999', '$200,000 or More']
        y_axis = list(worksheet.iloc[0])
    else:
        worksheet = df[df['County Name'] == value]
        if tablechoice == 'Monthly Rent':
            worksheet = worksheet[rent_variables]
            x_axis = ['Less than $500', '$500 - $999', '$1,000 - $1,499', '$1,500 - $1,999', '$2,000 - $2,499', '$2,500 - $2,999',
                    '$3,000 or More']
            y_axis = list(worksheet.iloc[0])
        elif tablechoice == 'Monthly Homeowner Costs (Mortgage)':
            worksheet = worksheet[homeownermort_variables]
            x_axis = ['Less than $500', '$500 - $999', '$1,000 - $1,499', '$1,500 - $1,999', '$2,000 - $2,499', '$2,500 - $2,999',
                    '$3,000 or More']
            y_axis = list(worksheet.iloc[0])
        else:
            worksheet = worksheet[homeownernomort_variables]
            x_axis = ['Less than $250', '$250 - $399', '$400 - $599', '$600 - $799', '$800 - $999', '$1,000 or More']
            y_axis = list(worksheet.iloc[0])
    fig15 = go.Figure(data=[go.Bar(x=x_axis, y=y_axis)])
    fig15.update_layout(
        yaxis=dict(
        title='Count of Households',
        titlefont_size=16,),
    )
    return fig15

##Household Assistance Table
@app.callback(
    dash.dependencies.Output('hh-assist', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hhassist(value):
    ###Pull Data
    ep1 = ep[ep['County Name'] == value]
    ep2 = ep1[['DP03_0051E','DP03_0062E','DP03_0066E','DP03_0068E','DP03_0070E','DP03_0072E','DP03_0074E']]
    ep2.columns = ['totalhh', 'medHHinc', 'totalhhssec', 'totalhhretire', 'totalhhssi', 'totalhhcash', 'totalhhsnap']
   
    ###Calculations
    ep2['%ssec'] = ep2['totalhhssec']/ep2['totalhh']
    ep2['%retire'] = ep2['totalhhretire']/ep2['totalhh']
    ep2['%ssi'] = ep2['totalhhssi']/ep2['totalhh']
    ep2['%cash'] = ep2['totalhhcash']/ep2['totalhh']
    ep2['%snap'] = ep2['totalhhsnap']/ep2['totalhh']
    ep2 = ep2[['%ssec', '%retire', '%ssi', '%cash', '%snap']]
    ep2['%ssec'] = ep2.apply(lambda x: "{:.1%}".format(float(x['%ssec'])), axis=1)
    ep2['%retire'] = ep2.apply(lambda x: "{:.1%}".format(float(x['%retire'])), axis=1)
    ep2['%ssi'] = ep2.apply(lambda x: "{:.1%}".format(float(x['%ssi'])), axis=1)
    ep2['%cash'] = ep2.apply(lambda x: "{:.1%}".format(float(x['%cash'])), axis=1)
    ep2['%snap'] = ep2.apply(lambda x: "{:.1%}".format(float(x['%snap'])), axis=1)
    epg = ep2.transpose()
    epg.columns = [' ']
    clab = ['% of Households on Social Security', '% of Households with Retirement Income' , '% of Households with SSI', 
        '% of Households Receiving Cash Assistance', '% of Households Receiving SNAP Benefits']
    epg.insert(0,'Household Income and Assistance', clab, True) 
    
    ###Create Table
    fig8 = ff.create_table(epg)
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
        yrs = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2015']
        hist2 = hist1.transpose()
        hist2 = hist2.iloc[3:]
        hist2.columns = ['Population']
        hist2.insert(0,'Year', yrs, True)

        ###Create Graph
        fig9 = go.Figure(data=go.Scatter(x=hist2['Year'], y=hist2['Population']))
        fig9.update_layout(title='Total Population over Time',
                    xaxis_title='Year',
                    yaxis_title='Population Count')
        return fig9
    else:
        return no_data_fig

##Household Size
@app.callback(
    dash.dependencies.Output('hhsize', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_hhsize(value):
    ###Pull and Collate Data
    hhs1 = hhs[hhs['NAME'] == value]
    hhs2 = hhs1[['1p_hh',
        '2p_hh',
        '3p_hh',
        '4+'
    ]]
    hsize = ['1 Person Households', '2 Person Households', '3 Person Households', '4 + Person Households']
    hhs3 = hhs2.transpose()
    hhs3.columns = ['# of Households']
    hhs3.insert(0, 'Household Size', hsize, True)

    ###Create Graph
    fig14 = px.bar(hhs3, x='Household Size', y='# of Households')
    return fig14

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
    fig10 = make_subplots(shared_xaxes=False,
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


##Population by Race
@app.callback(
    dash.dependencies.Output('race-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_race(value):
    ###Pull and Collate Data
    tr = tp[tp['County Name'] == value]
    tr1 = tr[['DP05_0077E','DP05_0078E','DP05_0071E','DP05_0079E','DP05_0080E','DP05_0081E','DP05_0082E','DP05_0083E']]
    race = ['White', 'Black', 'Latinx', 'Native American/Alaskan Native', 'Asian', 'Hawaiian/Pacific Islander', 'Other Race',
    'Two or More Races']
    tr2 = tr1.transpose()
    tr2.columns = ['Population Count']
    tr2.insert(0,'Population by Race', race, True)
    
    ###Create Graph
    fig25 = px.bar(tr2, x='Population by Race', y='Population Count')
    return fig25


##Population by Sex
@app.callback(
    dash.dependencies.Output('sex-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_sex(value):
    ###Pull and Collate Data
    ts = tp[tp['County Name'] == value]
    ts1 = ts[['SEX AND AGE_Total population_Male_Estimate',
    'SEX AND AGE_Total population_Female_Estimate']]
    sex = ['Male', 'Female']
    ts2 = ts1.transpose()
    ts2.columns = ['Population Count']
    ts2.insert(0,'Population by Sex', sex, True) 

    ###Create Graph
    fig12 = px.bar(ts2, x='Population by Sex', y='Population Count')
    return fig12

##Special Populations Table
@app.callback(
    dash.dependencies.Output('spec-g', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_special(value):
    ###Pull and Collate Data
    dp1 = dp[dp['County Name'] == value]
    dp2 = dp1[['DP02_0001E','DP02_0007E','DP02_0011E','DP02_0071E','DP02_0072E','DP02_0077E','DP02_0078E','DP02_0111E','DP02_0114E']]
    sparenthh = (dp2['DP02_0007E']+dp2['DP02_0011E'])
    dp2['% Single Parent Households'] = sparenthh/dp2['DP02_0001E']      
    dp2['% of People with Disabilities'] = dp2['DP02_0072E']/dp2['DP02_0071E']
    dp2['% of Individuals 65 and Over with Disabilities'] = dp2['DP02_0078E']/dp2['DP02_0077E']
    dp2['% of Non-Fluent English Speakers'] = dp2['DP02_0114E']/dp2['DP02_0111E']
    dp3 = dp2[['% Single Parent Households', '% of People with Disabilities', '% of Individuals 65 and Over with Disabilities', '% of Non-Fluent English Speakers']]
    dp3['% Single Parent Households'] = dp3.apply(lambda x: "{:.1%}".format(x['% Single Parent Households']), axis=1)
    dp3['% of People with Disabilities'] = dp3.apply(lambda x: "{:.1%}".format(x['% of People with Disabilities']), axis=1)
    dp3['% of Individuals 65 and Over with Disabilities'] = dp3.apply(lambda x: "{:.1%}".format(x['% of Individuals 65 and Over with Disabilities']), axis=1)
    dp3['% of Non-Fluent English Speakers'] = dp3.apply(lambda x: "{:.1%}".format(x['% of Non-Fluent English Speakers']), axis=1)
    dp4 = dp3.transpose()
    hhs = ['% of Single Parent Households', '% of People with a Disability', '% of Individuals 65 and Over with a Disability', '% of Non-Fluent English Speakers']
    dp4.columns = [' ']
    dp4.insert(0,'Special Populations', hhs, True) 


    ###Create Table
    fig12 = ff.create_table(dp4)
    return fig12

if __name__ == '__main__':
    app.run_server(debug=True)
