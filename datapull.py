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
import json
import requests
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
import csv

#Set Year
year1 = 2018

# Base path to data files
base_path = Path(__file__).resolve().parent / "data"
census_path = base_path / "census_data"
hud_path = base_path / "hud_prog_data"
chas_path = base_path / "CHAS_data"
pop_path =  base_path / "pop_proj" / "hist_d"

#Pull in Data Mapping File
acs_map = pd.read_csv(str(base_path / "tpop_var.csv"))
age_g = pd.read_csv(str(base_path / "group_list.csv"))

#Pull in Baseline Growth Elements
url1 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001B)&for=county:*".format(year1)
url2 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001C)&for=county:*".format(year1)
url3 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001D)&for=county:*".format(year1)
url4 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001E)&for=county:*".format(year1)
url5 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001F)&for=county:*".format(year1)
url6 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001G)&for=county:*".format(year1)
url7 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001H)&for=county:*".format(year1)
url8 = "https://api.census.gov/data/{}/acs/acs5?key=54690f8093283c11c9612c58bc15b56ba3a26373&get=NAME,group(B01001I)&for=county:*".format(year1)
acs1 = requests.get(url1)
acs2 = requests.get(url2)
acs3 = requests.get(url3)
acs4 = requests.get(url4)
acs5 = requests.get(url5)
acs6 = requests.get(url6)
acs7 = requests.get(url7)
acs8 = requests.get(url8)
sar1 = json.loads(acs1.text)
sar2 = json.loads(acs2.text)
sar3 = json.loads(acs3.text)
sar4 = json.loads(acs4.text)
sar5 = json.loads(acs5.text)
sar6 = json.loads(acs6.text)
sar7 = json.loads(acs7.text)
sar8 = json.loads(acs8.text)
df1 = pd.DataFrame(sar1,columns=sar1[0])
df2 = pd.DataFrame(sar2[1:],columns=sar2[0])
df3 = pd.DataFrame(sar3[1:],columns=sar3[0])
df4 = pd.DataFrame(sar4[1:],columns=sar4[0])
df5 = pd.DataFrame(sar5[1:],columns=sar5[0])
df6 = pd.DataFrame(sar6[1:],columns=sar6[0])
df7 = pd.DataFrame(sar7[1:],columns=sar7[0])
df8 = pd.DataFrame(sar8[1:],columns=sar8[0])
df1 = df1[['NAME','state','county','B01001B_003E','B01001B_004E','B01001B_005E','B01001B_006E','B01001B_007E',
    'B01001B_008E','B01001B_009E','B01001B_010E','B01001B_011E', 'B01001B_012E','B01001B_013E','B01001B_014E','B01001B_015E',
    'B01001B_016E','B01001B_018E','B01001B_019E','B01001B_020E','B01001B_021E','B01001B_022E','B01001B_023E',
    'B01001B_024E','B01001B_025E','B01001B_026E','B01001B_027E','B01001B_028E','B01001B_029E','B01001B_030E',
    'B01001B_031E']]

df2 = df2[['NAME','state','county','B01001C_003E','B01001C_004E','B01001C_005E','B01001C_006E','B01001C_007E',
    'B01001C_008E','B01001C_009E','B01001C_010E','B01001C_011E','B01001C_012E','B01001C_013E','B01001C_014E',
    'B01001C_015E','B01001C_016E','B01001C_018E','B01001C_019E','B01001C_020E','B01001C_021E','B01001C_022E',
    'B01001C_023E','B01001C_024E','B01001C_025E','B01001C_026E','B01001C_027E','B01001C_028E','B01001C_029E',
    'B01001C_030E','B01001C_031E']]

df3 = df3[['NAME','state','county','B01001D_003E','B01001D_004E','B01001D_005E','B01001D_006E','B01001D_007E',
    'B01001D_008E','B01001D_009E','B01001D_010E','B01001D_011E','B01001D_012E','B01001D_013E','B01001D_014E',
    'B01001D_015E','B01001D_016E','B01001D_018E','B01001D_019E','B01001D_020E','B01001D_021E','B01001D_022E',
    'B01001D_023E','B01001D_024E','B01001D_025E','B01001D_026E','B01001D_027E','B01001D_028E','B01001D_029E',
    'B01001D_030E','B01001D_031E']]

df4 = df4[['NAME','state','county','B01001E_003E','B01001E_004E','B01001E_005E','B01001E_006E','B01001E_007E',
    'B01001E_008E','B01001E_009E','B01001E_010E','B01001E_011E','B01001E_012E','B01001E_013E','B01001E_014E',
    'B01001E_015E','B01001E_016E','B01001E_018E','B01001E_019E','B01001E_020E','B01001E_021E','B01001E_022E',
    'B01001E_023E','B01001E_024E','B01001E_025E','B01001E_026E','B01001E_027E','B01001E_028E','B01001E_029E',
    'B01001E_030E','B01001E_031E']]

df5 = df5[['NAME','state','county','B01001F_003E','B01001F_004E','B01001F_005E','B01001F_006E','B01001F_007E',
    'B01001F_008E','B01001F_009E','B01001F_010E','B01001F_011E','B01001F_012E','B01001F_013E','B01001F_014E',
    'B01001F_015E','B01001F_016E','B01001F_018E','B01001F_019E','B01001F_020E','B01001F_021E','B01001F_022E',
    'B01001F_023E','B01001F_024E','B01001F_025E','B01001F_026E','B01001F_027E','B01001F_028E','B01001F_029E',
    'B01001F_030E','B01001F_031E']]

df6 = df6[['NAME','state','county','B01001G_003E','B01001G_004E','B01001G_005E','B01001G_006E','B01001G_007E',
    'B01001G_008E','B01001G_009E','B01001G_010E','B01001G_011E','B01001G_012E','B01001G_013E','B01001G_014E',
    'B01001G_015E','B01001G_016E','B01001G_018E','B01001G_019E','B01001G_020E','B01001G_021E','B01001G_022E',
    'B01001G_023E','B01001G_024E','B01001G_025E','B01001G_026E','B01001G_027E','B01001G_028E','B01001G_029E',
    'B01001G_030E','B01001G_031E']]

df7 = df7[['NAME','state','county','B01001H_003E','B01001H_004E','B01001H_005E','B01001H_006E','B01001H_007E',
    'B01001H_008E','B01001H_009E','B01001H_010E','B01001H_011E','B01001H_012E','B01001H_013E','B01001H_014E',
    'B01001H_015E','B01001H_016E','B01001H_018E','B01001H_019E','B01001H_020E','B01001H_021E','B01001H_022E',
    'B01001H_023E','B01001H_024E','B01001H_025E','B01001H_026E','B01001H_027E','B01001H_028E','B01001H_029E',
    'B01001H_030E','B01001H_031E']]

df8 = df8[['NAME','state','county','B01001I_003E','B01001I_004E','B01001I_005E','B01001I_006E','B01001I_007E',
    'B01001I_008E','B01001I_009E','B01001I_010E','B01001I_011E','B01001I_012E','B01001I_013E','B01001I_014E',
    'B01001I_015E','B01001I_016E','B01001I_018E','B01001I_019E','B01001I_020E','B01001I_021E','B01001I_022E',
    'B01001I_023E','B01001I_024E','B01001I_025E','B01001I_026E','B01001I_027E','B01001I_028E','B01001I_029E',
    'B01001I_030E','B01001I_031E']]

df1 = df1.loc[:,~df1.columns.duplicated()]
df2 = df2.loc[:,~df2.columns.duplicated()]
df3 = df3.loc[:,~df3.columns.duplicated()]
df4 = df4.loc[:,~df4.columns.duplicated()]
df5 = df5.loc[:,~df5.columns.duplicated()]
df6 = df6.loc[:,~df6.columns.duplicated()]
df7 = df7.loc[:,~df7.columns.duplicated()]
df8 = df8.loc[:,~df8.columns.duplicated()]
dfc = df1
df_2 = df2.drop(['state', 'county'], axis=1)
df_3 = df3.drop(['state', 'county'], axis=1)
df_4 = df4.drop(['state', 'county'], axis=1)
df_5 = df5.drop(['state', 'county'], axis=1)
df_6 = df6.drop(['state', 'county'], axis=1)
df_7 = df7.drop(['state', 'county'], axis=1)
df_8 = df8.drop(['state', 'county'], axis=1)
dfc = dfc.merge(df_2, on='NAME', how='left')
dfc = dfc.merge(df_3, on='NAME', how='left')
dfc = dfc.merge(df_4, on='NAME', how='left')
dfc = dfc.merge(df_5, on='NAME', how='left')
dfc = dfc.merge(df_6, on='NAME', how='left')
dfc = dfc.merge(df_7, on='NAME', how='left')
dfc = dfc.merge(df_8, on='NAME', how='left')
keys = list(acs_map['NAME'])
values = list(acs_map['NAME.1'])
mydict = dict(zip(keys, values))
est = dfc
col_head = col_head = list(est)
new_col = [mydict.get(item,item) for item in col_head]
est.columns = new_col
young = ['Black_Male15_17','Black_Male18_19','Black_Female15_17','Black_Female18_19','NA_AN_Male15_17',
    'NA_AN_Male18_19','NA_AN_Female15_17','NA_AN_Female18_19','Asian_Male15_17','Asian_Male18_19',
    'Asian_Male18_19','Asian_Female15_17','Asian_Female18_19','Asian_Female18_19','NH_API_Male15_17',
    'NH_API_Male18_19','NH_API_Female15_17','NH_API_Female18_19','NH_API_Female18_19','Other_Male15_17',
    'Other_Male18_19','Other_Female15_17','Other_Female18_19','Multiple_Male15_17','Multiple_Male18_19',
    'Multiple_Female15_17','Multiple_Female18_19','White_Male15_17','White_Male18_19','White_Female15_17',
    'White_Female18_19','Latinx_Male15_17','Latinx_Male18_19','Latinx_Female15_17','Latinx_Female18_19']
ccol = new_col[3:]
est[ccol] = est[ccol].apply(pd.to_numeric, errors='coerce').fillna(0)
est['Black_Male15_19'] = est['Black_Male15_17'] + est['Black_Male18_19']
est['Black_Female15_19'] = est['Black_Female15_17'] + est['Black_Female18_19']
est['NA_AN_Male15_19'] = est['NA_AN_Male15_17'] + est['NA_AN_Male18_19']
est['NA_AN_Female15_19'] = est['NA_AN_Female15_17'] + est['NA_AN_Female18_19']
est['Asian_Male15_19'] = est['Asian_Male15_17'] + est['Asian_Male18_19']
est['Asian_Female15_19'] = est['Asian_Female15_17'] + est['Asian_Female18_19']
est['NH_API_Male15_19'] = est['NH_API_Male15_17'] + est['NH_API_Male18_19']
est['NH_API_Female15_19'] = est['NH_API_Female15_17'] + est['NH_API_Female18_19']
est['Other_Male15_19'] = est['Other_Male15_17'] + est['Other_Male18_19']
est['Other_Female15_19'] = est['Other_Female15_17'] + est['Other_Female18_19']
est['Multiple_Male15_19'] = est['Multiple_Male15_17'] + est['Multiple_Male18_19']
est['Multiple_Female15_19'] = est['Multiple_Female15_17'] + est['Multiple_Female18_19']
est['White_Male15_19'] = est['White_Male15_17'] + est['White_Male18_19']
est['White_Female15_19'] = est['White_Female15_17'] + est['White_Female18_19']
est['Latinx_Male15_19'] = est['Latinx_Male15_17'] + est['Latinx_Male18_19']
est['Latinx_Female15_19'] = est['Latinx_Female15_17'] + est['Latinx_Female18_19']
est = est.drop(young, axis=1)
est1 = est.drop(['state', 'county'], axis=1)
grp = list(est1)
grp = grp[1:]
est2 = est1.transpose()
est2.columns = est2.iloc[0]
PLACES = list(est2)
est3 = est2.iloc[1:]
est3.insert(0,'map',grp,True)
est3 = est3.merge(age_g, on='map', how='left')
est4 = est3.groupby(["age","sex"]).sum()
est5 = est4
est5.reset_index(level=est5.index.names, inplace=True)
est5 = est5.drop('map',axis=1)

est5.to_csv(str(base_path /"today.csv"), encoding='utf-8', index=False)
print('Data Pulled: ACS Population 5-year Estimates for {}'.format(year1))




