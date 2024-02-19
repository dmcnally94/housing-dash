import pandas as pd
import os
import locale
import json
import requests
import csv
from pathlib import Path
import datetime
import zipfile
import io
import numpy as np
import geopandas as gpd
import esridumpgdf
from esridumpgdf import Layer
from dotenv import load_dotenv

#ESRI AGOL Script to import Data
def esri_import(x):
    layer = Layer(x).to_gdf()
    return layer

#Presets (Check to Update)
current_year = datetime.date.today().year
year_minus1 = current_year-1
year_minus2 = year_minus1-1
year_minus3 = year_minus2-1
year_minus4 = year_minus3-1
load_dotenv()
CENSUS_KEY = os.getenv('CENSUS_KEY')

#ACS Year Test
if requests.get("https://api.census.gov/data/{}/acs/{}?get=NAME,B01001_001E&for={}:{}&key={}".format(year_minus1, 'acs5','state','*',CENSUS_KEY)).status_code == 200:
    year = year_minus1
elif requests.get("https://api.census.gov/data/{}/acs/{}?get=NAME,B01001_001E&for={}:{}&key={}".format(year_minus2, 'acs5','state','*',CENSUS_KEY)).status_code == 200:
    year = year_minus2
elif requests.get("https://api.census.gov/data/{}/acs/{}?get=NAME,B01001_001E&for={}:{}&key={}".format(year_minus3, 'acs5','state','*',CENSUS_KEY)).status_code == 200:
    year = year_minus3
elif requests.get("https://api.census.gov/data/{}/acs/{}?get=NAME,B01001_001E&for={}:{}&key={}".format(year_minus4, 'acs5','state','*',CENSUS_KEY)).status_code == 200:
    year = year_minus4
else:
    print('ACS ERROR: NO SUITABLE YEAR')

#CHAS Year Test
if requests.get('https://www.huduser.gov/portal/datasets/cp/'+str(year_minus1-4)+'thru'+str(year_minus1)+'-160-csv.zip').status_code == 200:
    chas_year = year_minus1
elif requests.get('https://www.huduser.gov/portal/datasets/cp/'+str(year_minus2-4)+'thru'+str(year_minus2)+'-160-csv.zip').status_code == 200:
    chas_year = year_minus2
elif requests.get('https://www.huduser.gov/portal/datasets/cp/'+str(year_minus3-4)+'thru'+str(year_minus3)+'-160-csv.zip').status_code == 200:
    chas_year = year_minus3
elif requests.get('https://www.huduser.gov/portal/datasets/cp/'+str(year_minus4-4)+'thru'+str(year_minus4)+'-050-csv.zip').status_code == 200:
    chas_year = year_minus4
else:
    print('CHAS ERROR: NO SUITABLE YEAR')


savename = "placedashdata.csv"
base_path = Path(__file__).resolve().parent
chas_path = base_path / "placeCHAS"
datadic = "/CHAS data dictionary 13-17.xlsx"
save_path = 'C:/projects/housing-dash/data/'
profiles = ['DP03', 'DP04', 'DP05']
geography = 'place'
geotype = '*'
censuskey = CENSUS_KEY


#Variables (Check Periodically)
unit_vacancy_variables = ['DP04_0001E','DP04_0003E','DP04_0004E','DP04_0005E','DP04_0046E','DP04_0047E']
unit_vacancy_var_names = ['Total Housing Units','Vacant Housing Units', 'Homeowner Vacancy Rate', 'Rental Vacancy Rate', 'Owner Occupied Units', 
                          'Renter Occupied Units']

unit_type_variables = ['DP04_0007E','DP04_0008E','DP04_0009E','DP04_0010E','DP04_0011E','DP04_0012E','DP04_0013E','DP04_0014E','DP04_0015E']
unit_type_var_names = ['Single Family, Detached', 'Single Family, Attached', 'Duplex Units', 'Triplex or Fourplex','Low Rise Multifamily (5-9 units)',
                       'Medium Rise Multifamily (10-19 units)', 'Large Multifamily (20+ units)','Mobile Home','Other (Boat, RV, van, etc.)']

unit_bedrooms_variables = ['DP04_0039E', 'DP04_0040E', 'DP04_0041E', 'DP04_0042E', 'DP04_0043E', 'DP04_0044E']
unit_bedrooms_var_names = ['Studio Units', '1 Bedroom Units', '2 Bedroom Units', '3 Bedroom Units','4 Bedroom Units','5+ Bedroom Units']

unit_age_variables = ['DP04_0017E','DP04_0018E','DP04_0019E','DP04_0020E', 'DP04_0021E','DP04_0022E', 'DP04_0023E', 'DP04_0024E', 'DP04_0025E','DP04_0026E']
unit_age_var_names = ['Units Built 2014 and Later','Units Built Between 2010 and 2013','Units Built Between 2000 and 2009','Units Built Between 1990 and 1999',
                      'Units Built Between 1980 and 1989','Units Built Between 1970 and 1979','Units Built Between 1960 and 1969',
                      'Units Built Between 1950 and 1959','Units Built Between 1940 and 1949','Units Built 1939 or Earlier']

housing_cost_variables = ['DP03_0062E','DP04_0089E','DP04_0134E','DP04_0101E','DP04_0109E']
housing_cost_var_names = ['Median Household Income', 'Median Home Value', 'Median Gross Rent', 'Median Monthly Owner Costs (Mortgage)',
                          'Median Monthly Owner Costs (No Mortgage)']

unit_rent_variables = ['DP04_0127E', 'DP04_0128E', 'DP04_0129E','DP04_0130E', 'DP04_0131E', 'DP04_0132E','DP04_0133E']
unit_rent_var_names = ['Rent Less than $500', 'Rent $500 - $999', 'Rent $1,000 - $1,499', 'Rent $1,500 - $1,999', 'Rent $2,000 - $2,499', 
                       'Rent $2,500 - $2,999', 'Rent $3,000 or More']

unit_mort_variables = ['DP04_0094E','DP04_0095E','DP04_0096E','DP04_0097E','DP04_0098E','DP04_0099E','DP04_0100E']
unit_mort_var_names = ['Mortgage Less than $500', 'Mortgage $500 - $999', 'Mortgage $1,000 - $1,499', 'Mortgage $1,500 - $1,999', 
                       'Mortgage $2,000 - $2,499', 'Mortgage $2,500 - $2,999', 'Mortgage $3,000 or More']

unit_nomort_variables = ['DP04_0103E','DP04_0104E','DP04_0105E','DP04_0106E','DP04_0107E','DP04_0108E']
unit_nomort_var_names = ['Homeowner Costs Less than $250', 'Homeowner Costs $250 - $399', 'Homeowner Costs $400 - $599', 
                         'Homeowner Costs $600 - $799', 'Homeowner Costs $800 - $999', 'Homeowner Costs $1,000 or More']

hhincome_variables = ['DP03_0052E','DP03_0053E','DP03_0054E','DP03_0055E','DP03_0056E','DP03_0057E','DP03_0058E','DP03_0059E', 'DP03_0060E','DP03_0061E']
hhincome_var_names = ['HH Income Less than $10,000', 'HH Income $10,000 - $14,999', 'HH Income $15,000 - $24,999', 'HH Income $25,000 - $34,999', 
                      'HH Income $35,000 - $49,999', 'HH Income $50,000 - $74,999', 'HH Income $75,000 - $99,999', 'HH Income $100,000 - $149,999', 
                      'HH Income $150,000 - $199,999', 'HH Income $200,000 or More']

hhassistance_variables = ['DP03_0051E','DP03_0066E','DP03_0068E','DP03_0070E','DP03_0072E','DP03_0074E']
hhassistance_var_names = ['Total Households (HH Assistance)', 'Households Receiving Social Security', 'Households Receiveing Retirement Income',
                          'Households Receiving SSI', 'Households Receiving Cash Assistance', 'Households Receiving SNAP Benefits']

race_variables = ['DP05_0077E','DP05_0078E','DP05_0071E','DP05_0079E','DP05_0080E','DP05_0081E','DP05_0082E','DP05_0083E']
race_var_names = ['White', 'Black', 'Latinx', 'Native American/Alaskan Native', 'Asian', 'Hawaiian/Pacific Islander', 'Other Race',
                  'Two or More Races']

sex_variables = ['DP05_0002E','DP05_0003E']
sex_var_names = ['Male Population', 'Female Population']

specialgroups_variables = ['DP02_0001E','DP02_0007E','DP02_0011E','DP02_0071E','DP02_0072E','DP02_0077E','DP02_0078E','DP02_0111E','DP02_0114E']
specialgroups_var_names = ['Total Households', 'Single Male Parent Household', 'Single Female Parent Household', 'Total Civilian Population', 
                          'Total Civilian Population with a Disability', 'Civilian Population 65 year and Older', 
                           'Civilian Population 65 year and Older with a Disability', 'Population 5 years and Older', 
                           'Population 5 years and Older who speak English less than very well']

today_pop_variable = ['DP05_0001E']
today_pop_var_name = ['Total Population']

hhsize_variables = ['S2501_C01_001E','S2501_C01_002E','S2501_C01_003E','S2501_C01_004E','S2501_C01_005E']
hhsize_var_names = ['Occupied Households', '1 Person Households', '2 Person Households', '3 Person Households', '4+ Person Households']

variables = [unit_vacancy_variables,unit_type_variables,unit_bedrooms_variables,unit_age_variables,housing_cost_variables,unit_rent_variables,
            unit_mort_variables,unit_nomort_variables,hhincome_variables,hhassistance_variables,race_variables,sex_variables,
             specialgroups_variables,today_pop_variable]

variable_names = [unit_vacancy_var_names, unit_type_var_names,unit_bedrooms_var_names,unit_age_var_names,housing_cost_var_names,unit_rent_var_names,
                  unit_mort_var_names,unit_nomort_var_names,hhincome_var_names,hhassistance_var_names,race_var_names,sex_var_names,specialgroups_var_names,
                  today_pop_var_name]

whitepop_variables = ['GEO_ID','B01001H_003E','B01001H_004E','B01001H_005E','B01001H_006E','B01001H_007E',
                      'B01001H_008E','B01001H_009E','B01001H_010E','B01001H_011E','B01001H_012E','B01001H_013E','B01001H_014E',
                      'B01001H_015E','B01001H_016E','B01001H_018E','B01001H_019E','B01001H_020E','B01001H_021E','B01001H_022E',
                      'B01001H_023E','B01001H_024E','B01001H_025E','B01001H_026E','B01001H_027E','B01001H_028E','B01001H_029E','B01001H_030E','B01001H_031E']

whitepop_var_names = ['GEO_ID', 'White Male 0-4 years', 'White Male 5-9 years','White Male 10-14 years','White Male 15-17 years','White Male 18-19 years',
                     'White Male 20-24 years','White Male 25-29 years','White Male 30-34 years','White Male 35-44 years',
                      'White Male 45-54 years','White Male 55-64 years','White Male 65-74 years','White Male 75-84 years','White Male 85 years +',
                     'White Female 0-4 years', 'White Female 5-9 years','White Female 10-14 years','White Female 15-17 years','White Female 18-19 years',
                     'White Female 20-24 years','White Female 25-29 years','White Female 30-34 years','White Female 35-44 years',
                      'White Female 45-54 years','White Female 55-64 years','White Female 65-74 years','White Female 75-84 years','White Female 85 years +']

blackpop_variables = ['GEO_ID','B01001B_003E','B01001B_004E','B01001B_005E','B01001B_006E','B01001B_007E',
                      'B01001B_008E','B01001B_009E','B01001B_010E','B01001B_011E', 'B01001B_012E','B01001B_013E','B01001B_014E','B01001B_015E',
                      'B01001B_016E','B01001B_018E','B01001B_019E','B01001B_020E','B01001B_021E','B01001B_022E','B01001B_023E',
                      'B01001B_024E','B01001B_025E','B01001B_026E','B01001B_027E','B01001B_028E','B01001B_029E','B01001B_030E','B01001B_031E']

blackpop_var_names = ['GEO_ID', 'Black Male 0-4 years', 'Black Male 5-9 years','Black Male 10-14 years','Black Male 15-17 years','Black Male 18-19 years',
                     'Black Male 20-24 years','Black Male 25-29 years','Black Male 30-34 years','Black Male 35-44 years',
                      'Black Male 45-54 years','Black Male 55-64 years','Black Male 65-74 years','Black Male 75-84 years','Black Male 85 years +',
                     'Black Female 0-4 years', 'Black Female 5-9 years','Black Female 10-14 years','Black Female 15-17 years','Black Female 18-19 years',
                     'Black Female 20-24 years','Black Female 25-29 years','Black Female 30-34 years','Black Female 35-44 years',
                      'Black Female 45-54 years','Black Female 55-64 years','Black Female 65-74 years','Black Female 75-84 years','Black Female 85 years +']

nativepop_variables = ['GEO_ID','B01001C_003E','B01001C_004E','B01001C_005E','B01001C_006E','B01001C_007E','B01001C_008E',
                      'B01001C_009E','B01001C_010E','B01001C_011E','B01001C_012E','B01001C_013E','B01001C_014E','B01001C_015E','B01001C_016E',
                      'B01001C_018E','B01001C_019E','B01001C_020E','B01001C_021E','B01001C_022E','B01001C_023E','B01001C_024E','B01001C_025E',
                      'B01001C_026E','B01001C_027E','B01001C_028E','B01001C_029E','B01001C_030E','B01001C_031E']

nativepop_var_names = ['GEO_ID', 'Native American Male 0-4 years', 'Native American Male 5-9 years','Native American Male 10-14 years',
                       'Native American Male 15-17 years','Native American Male 18-19 years','Native American Male 20-24 years','Native American Male 25-29 years',
                       'Native American Male 30-34 years','Native American Male 35-44 years','Native American Male 45-54 years',
                       'Native American Male 55-64 years','Native American Male 65-74 years','Native American Male 75-84 years','Native American Male 85 years +',
                       'Native American Female 0-4 years', 'Native American Female 5-9 years','Native American Female 10-14 years',
                       'Native American Female 15-17 years','Native American Female 18-19 years','Native American Female 20-24 years',
                       'Native American Female 25-29 years','Native American Female 30-34 years','Native American Female 35-44 years',
                       'Native American Female 45-54 years','Native American Female 55-64 years',
                       'Native American Female 65-74 years','Native American Female 75-84 years','Native American Female 85 years +']

asianpop_variables = ['GEO_ID','B01001D_003E','B01001D_004E','B01001D_005E','B01001D_006E','B01001D_007E','B01001D_008E','B01001D_009E',
                      'B01001D_010E','B01001D_011E','B01001D_012E','B01001D_013E','B01001D_014E','B01001D_015E','B01001D_016E','B01001D_018E',
                      'B01001D_019E','B01001D_020E','B01001D_021E','B01001D_022E','B01001D_023E','B01001D_024E','B01001D_025E','B01001D_026E',
                      'B01001D_027E','B01001D_028E','B01001D_029E','B01001D_030E','B01001D_031E']

asianpop_var_names = ['GEO_ID', 'Asian Male 0-4 years', 'Asian Male 5-9 years','Asian Male 10-14 years','Asian Male 15-17 years',
                      'Asian Male 18-19 years','Asian Male 20-24 years','Asian Male 25-29 years','Asian Male 30-34 years','Asian Male 35-44 years',
                      'Asian Male 45-54 years','Asian Male 55-64 years','Asian Male 65-74 years','Asian Male 75-84 years',
                      'Asian Male 85 years +','Asian Female 0-4 years', 'Asian Female 5-9 years','Asian Female 10-14 years','Asian Female 15-17 years',
                      'Asian Female 18-19 years','Asian Female 20-24 years','Asian Female 25-29 years','Asian Female 30-34 years','Asian Female 35-44 years',
                      'Asian Female 45-54 years','Asian Female 55-64 years','Asian Female 65-74 years',
                      'Asian Female 75-84 years','Asian Female 85 years +']

pacificpop_variables = ['GEO_ID','B01001E_003E','B01001E_004E','B01001E_005E','B01001E_006E','B01001E_007E','B01001E_008E','B01001E_009E','B01001E_010E',
                        'B01001E_011E','B01001E_012E','B01001E_013E','B01001E_014E','B01001E_015E','B01001E_016E','B01001E_018E','B01001E_019E','B01001E_020E',
                        'B01001E_021E','B01001E_022E','B01001E_023E','B01001E_024E','B01001E_025E','B01001E_026E','B01001E_027E','B01001E_028E','B01001E_029E',
                        'B01001E_030E','B01001E_031E']

pacificpop_var_names = ['GEO_ID', 'Hawaiian or Pacific Islander Male 0-4 years', 'Hawaiian or Pacific Islander Male 5-9 years','Hawaiian or Pacific Islander Male 10-14 years','Hawaiian or Pacific Islander Male 15-17 years',
                      'Hawaiian or Pacific Islander Male 18-19 years','Hawaiian or Pacific Islander Male 20-24 years',
                        'Hawaiian or Pacific Islander Male 25-29 years','Hawaiian or Pacific Islander Male 30-34 years',
                        'Hawaiian or Pacific Islander Male 35-44 years',
                        'Hawaiian or Pacific Islander Male 45-54 years','Hawaiian or Pacific Islander Male 55-64 years',
                        'Hawaiian or Pacific Islander Male 65-74 years','Hawaiian or Pacific Islander Male 75-84 years',
                        'Hawaiian or Pacific Islander Male 85 years +','Hawaiian or Pacific Islander Female 0-4 years', 
                        'Hawaiian or Pacific Islander Female 5-9 years','Hawaiian or Pacific Islander Female 10-14 years',
                        'Hawaiian or Pacific Islander Female 15-17 years','Hawaiian or Pacific Islander Female 18-19 years',
                        'Hawaiian or Pacific Islander Female 20-24 years','Hawaiian or Pacific Islander Female 25-29 years',
                        'Hawaiian or Pacific Islander Female 30-34 years','Hawaiian or Pacific Islander Female 35-44 years',
                        'Hawaiian or Pacific Islander Female 45-54 years',
                        'Hawaiian or Pacific Islander Female 55-64 years','Hawaiian or Pacific Islander Female 65-74 years',
                      'Hawaiian or Pacific Islander Female 75-84 years','Hawaiian or Pacific Islander Female 85 years +']

otherpop_variables = ['GEO_ID','B01001F_003E','B01001F_004E','B01001F_005E','B01001F_006E','B01001F_007E','B01001F_008E','B01001F_009E',
                      'B01001F_010E','B01001F_011E','B01001F_012E','B01001F_013E','B01001F_014E','B01001F_015E','B01001F_016E','B01001F_018E',
                      'B01001F_019E','B01001F_020E','B01001F_021E','B01001F_022E','B01001F_023E','B01001F_024E','B01001F_025E','B01001F_026E','B01001F_027E',
                      'B01001F_028E','B01001F_029E','B01001F_030E','B01001F_031E']

otherpop_var_names = ['GEO_ID', 'Other Male 0-4 years', 'Other Male 5-9 years','Other Male 10-14 years','Other Male 15-17 years',
                      'Other Male 18-19 years','Other Male 20-24 years','Other Male 25-29 years','Other Male 30-34 years','Other Male 35-44 years',
                      'Other Male 45-54 years','Other Male 55-64 years','Other Male 65-74 years','Other Male 75-84 years',
                      'Other Male 85 years +','Other Female 0-4 years', 'Other Female 5-9 years','Other Female 10-14 years','Other Female 15-17 years',
                      'Other Female 18-19 years','Other Female 20-24 years','Other Female 25-29 years','Other Female 30-34 years','Other Female 35-44 years',
                      'Other Female 45-54 years','Other Female 55-64 years','Other Female 65-74 years',
                      'Other Female 75-84 years','Other Female 85 years +']

multipop_variables = ['GEO_ID','B01001G_003E','B01001G_004E','B01001G_005E','B01001G_006E','B01001G_007E','B01001G_008E','B01001G_009E','B01001G_010E',
                      'B01001G_011E','B01001G_012E','B01001G_013E','B01001G_014E','B01001G_015E','B01001G_016E','B01001G_018E','B01001G_019E','B01001G_020E',
                      'B01001G_021E','B01001G_022E','B01001G_023E','B01001G_024E','B01001G_025E','B01001G_026E','B01001G_027E','B01001G_028E','B01001G_029E',
                      'B01001G_030E','B01001G_031E']

multipop_var_names = ['GEO_ID', 'Multiracial Male 0-4 years', 'Multiracial Male 5-9 years','Multiracial Male 10-14 years','Multiracial Male 15-17 years',
                      'Multiracial Male 18-19 years','Multiracial Male 20-24 years','Multiracial Male 25-29 years','Multiracial Male 30-34 years',
                      'Multiracial Male 35-44 years','Multiracial Male 45-54 years','Multiracial Male 55-64 years',
                      'Multiracial Male 65-74 years','Multiracial Male 75-84 years','Multiracial Male 85 years +','Multiracial Female 0-4 years', 
                      'Multiracial Female 5-9 years','Multiracial Female 10-14 years','Multiracial Female 15-17 years','Multiracial Female 18-19 years',
                      'Multiracial Female 20-24 years','Multiracial Female 25-29 years','Multiracial Female 30-34 years','Multiracial Female 35-44 years',
                      'Multiracial Female 45-54 years','Multiracial Female 55-64 years','Multiracial Female 65-74 years',
                      'Multiracial Female 75-84 years','Multiracial Female 85 years +']

latinpop_variables = ['GEO_ID','B01001I_003E','B01001I_004E','B01001I_005E','B01001I_006E','B01001I_007E','B01001I_008E','B01001I_009E','B01001I_010E',
                      'B01001I_011E','B01001I_012E','B01001I_013E','B01001I_014E','B01001I_015E','B01001I_016E','B01001I_018E','B01001I_019E','B01001I_020E',
                      'B01001I_021E','B01001I_022E','B01001I_023E','B01001I_024E','B01001I_025E','B01001I_026E','B01001I_027E','B01001I_028E','B01001I_029E',
                      'B01001I_030E','B01001I_031E']

latinpop_var_names = ['GEO_ID', 'Latinx Male 0-4 years', 'Latinx Male 5-9 years','Latinx Male 10-14 years','Latinx Male 15-17 years',
                      'Latinx Male 18-19 years','Latinx Male 20-24 years','Latinx Male 25-29 years','Latinx Male 30-34 years','Latinx Male 35-44 years',
                      'Latinx Male 45-54 years','Latinx Male 55-64 years','Latinx Male 65-74 years','Latinx Male 75-84 years',
                      'Latinx Male 85 years +','Latinx Female 0-4 years', 'Latinx Female 5-9 years','Latinx Female 10-14 years','Latinx Female 15-17 years',
                      'Latinx Female 18-19 years','Latinx Female 20-24 years','Latinx Female 25-29 years','Latinx Female 30-34 years','Latinx Female 35-44 years',
                      'Latinx Female 45-54 years','Latinx Female 55-64 years','Latinx Female 65-74 years',
                      'Latinx Female 75-84 years','Latinx Female 85 years +']

malepop0to4 = ['White Male 0-4 years','Black Male 0-4 years','Native American Male 0-4 years','Asian Male 0-4 years','Hawaiian or Pacific Islander Male 0-4 years',
              'Other Male 0-4 years','Multiracial Male 0-4 years','Latinx Male 0-4 years']

malepop5to9 = ['White Male 5-9 years','Black Male 5-9 years','Native American Male 5-9 years','Asian Male 5-9 years','Hawaiian or Pacific Islander Male 5-9 years',
              'Other Male 5-9 years','Multiracial Male 5-9 years','Latinx Male 5-9 years']

malepop10to14 = ['White Male 10-14 years','Black Male 10-14 years','Native American Male 10-14 years','Asian Male 10-14 years','Hawaiian or Pacific Islander Male 10-14 years',
              'Other Male 10-14 years','Multiracial Male 10-14 years','Latinx Male 10-14 years']

malepop15to19 = ['White Male 15-19 years','Black Male 15-19 years','Native American Male 15-19 years','Asian Male 15-19 years','Hawaiian or Pacific Islander Male 15-19 years',
              'Other Male 15-19 years','Multiracial Male 15-19 years','Latinx Male 15-19 years']

malepop20to24 = ['White Male 20-24 years','Black Male 20-24 years','Native American Male 20-24 years','Asian Male 20-24 years','Hawaiian or Pacific Islander Male 20-24 years',
              'Other Male 20-24 years','Multiracial Male 20-24 years','Latinx Male 20-24 years']

malepop25to29 = ['White Male 25-29 years','Black Male 25-29 years','Native American Male 25-29 years','Asian Male 25-29 years','Hawaiian or Pacific Islander Male 25-29 years',
              'Other Male 25-29 years','Multiracial Male 25-29 years','Latinx Male 25-29 years']

malepop30to34 = ['White Male 30-34 years','Black Male 30-34 years','Native American Male 30-34 years','Asian Male 30-34 years','Hawaiian or Pacific Islander Male 30-34 years',
              'Other Male 30-34 years','Multiracial Male 30-34 years','Latinx Male 30-34 years']

malepop35to44 = ['White Male 35-44 years','Black Male 35-44 years','Native American Male 35-44 years','Asian Male 35-44 years','Hawaiian or Pacific Islander Male 35-44 years',
              'Other Male 35-44 years','Multiracial Male 35-44 years','Latinx Male 35-44 years']

malepop45to54 = ['White Male 45-54 years','Black Male 45-54 years','Native American Male 45-54 years','Asian Male 45-54 years','Hawaiian or Pacific Islander Male 45-54 years',
              'Other Male 45-54 years','Multiracial Male 45-54 years','Latinx Male 45-54 years']

malepop55to64 = ['White Male 55-64 years','Black Male 55-64 years','Native American Male 55-64 years','Asian Male 55-64 years','Hawaiian or Pacific Islander Male 55-64 years',
              'Other Male 55-64 years','Multiracial Male 55-64 years','Latinx Male 55-64 years']

malepop65to74 = ['White Male 65-74 years','Black Male 65-74 years','Native American Male 65-74 years','Asian Male 65-74 years','Hawaiian or Pacific Islander Male 65-74 years',
              'Other Male 65-74 years','Multiracial Male 65-74 years','Latinx Male 65-74 years']

malepop75to84 = ['White Male 75-84 years','Black Male 75-84 years','Native American Male 75-84 years','Asian Male 75-84 years','Hawaiian or Pacific Islander Male 75-84 years',
              'Other Male 75-84 years','Multiracial Male 75-84 years','Latinx Male 75-84 years']

malepop85up = ['White Male 85 years +','Black Male 85 years +','Native American Male 85 years +','Asian Male 85 years +','Hawaiian or Pacific Islander Male 85 years +',
              'Other Male 85 years +','Multiracial Male 85 years +','Latinx Male 85 years +']


femalepop0to4 = ['White Female 0-4 years','Black Female 0-4 years','Native American Female 0-4 years','Asian Female 0-4 years','Hawaiian or Pacific Islander Female 0-4 years',
              'Other Female 0-4 years','Multiracial Female 0-4 years','Latinx Female 0-4 years']

femalepop5to9 = ['White Female 5-9 years','Black Female 5-9 years','Native American Female 5-9 years','Asian Female 5-9 years','Hawaiian or Pacific Islander Female 5-9 years',
              'Other Female 5-9 years','Multiracial Female 5-9 years','Latinx Female 5-9 years']

femalepop10to14 = ['White Female 10-14 years','Black Female 10-14 years','Native American Female 10-14 years','Asian Female 10-14 years','Hawaiian or Pacific Islander Female 10-14 years',
              'Other Female 10-14 years','Multiracial Female 10-14 years','Latinx Female 10-14 years']

femalepop15to19 = ['White Female 15-19 years','Black Female 15-19 years','Native American Female 15-19 years','Asian Female 15-19 years','Hawaiian or Pacific Islander Female 15-19 years',
              'Other Female 15-19 years','Multiracial Female 15-19 years','Latinx Female 15-19 years']

femalepop20to24 = ['White Female 20-24 years','Black Female 20-24 years','Native American Female 20-24 years','Asian Female 20-24 years','Hawaiian or Pacific Islander Female 20-24 years',
              'Other Female 20-24 years','Multiracial Female 20-24 years','Latinx Female 20-24 years']

femalepop25to29 = ['White Female 25-29 years','Black Female 25-29 years','Native American Female 25-29 years','Asian Female 25-29 years','Hawaiian or Pacific Islander Female 25-29 years',
              'Other Female 25-29 years','Multiracial Female 25-29 years','Latinx Female 25-29 years']

femalepop30to34 = ['White Female 30-34 years','Black Female 30-34 years','Native American Female 30-34 years','Asian Female 30-34 years','Hawaiian or Pacific Islander Female 30-34 years',
              'Other Female 30-34 years','Multiracial Female 30-34 years','Latinx Female 30-34 years']

femalepop35to44 = ['White Female 35-44 years','Black Female 35-44 years','Native American Female 35-44 years','Asian Female 35-44 years','Hawaiian or Pacific Islander Female 35-44 years',
              'Other Female 35-44 years','Multiracial Female 35-44 years','Latinx Female 35-44 years']

femalepop45to54 = ['White Female 45-54 years','Black Female 45-54 years','Native American Female 45-54 years','Asian Female 45-54 years','Hawaiian or Pacific Islander Female 45-54 years',
              'Other Female 45-54 years','Multiracial Female 45-54 years','Latinx Female 45-54 years']

femalepop55to64 = ['White Female 55-64 years','Black Female 55-64 years','Native American Female 55-64 years','Asian Female 55-64 years','Hawaiian or Pacific Islander Female 55-64 years',
              'Other Female 55-64 years','Multiracial Female 55-64 years','Latinx Female 55-64 years']

femalepop65to74 = ['White Female 65-74 years','Black Female 65-74 years','Native American Female 65-74 years','Asian Female 65-74 years','Hawaiian or Pacific Islander Female 65-74 years',
              'Other Female 65-74 years','Multiracial Female 65-74 years','Latinx Female 65-74 years']

femalepop75to84 = ['White Female 75-84 years','Black Female 75-84 years','Native American Female 75-84 years','Asian Female 75-84 years','Hawaiian or Pacific Islander Female 75-84 years',
              'Other Female 75-84 years','Multiracial Female 75-84 years','Latinx Female 75-84 years']

femalepop85up = ['White Female 85 years +','Black Female 85 years +','Native American Female 85 years +','Asian Female 85 years +','Hawaiian or Pacific Islander Female 85 years +',
              'Other Female 85 years +','Multiracial Female 85 years +','Latinx Female 85 years +']

malepoplist = ['Male 0-4 years', 'Male 5-9 years','Male 10-14 years','Male 15-19 years',
               'Male 20-24 years','Male 25-29 years','Male 30-34 years','Male 35-44 years','Male 45-54 years',
               'Male 55-64 years','Male 65-74 years','Male 75-84 years','Male 85 years +']

femalepoplist = ['Female 0-4 years', 'Female 5-9 years','Female 10-14 years','Female 15-19 years',
               'Female 20-24 years','Female 25-29 years','Female 30-34 years','Female 35-44 years','Female 45-54 years',
               'Female 55-64 years','Female 65-74 years','Female 75-84 years','Female 85 years +']

racepoptotals = ['White Population', 'Black Population', 'Native American Population', 'Hawaiian or Pacific Islander Population', 'Asian Population',
                'Other Race Population', 'Multiracial Population', 'Latinx Population']

acs_variable_list = ['GEO_ID','NAME_y','state_y','place_y']

for i in variables:
    acs_variable_list.extend(i)

#ACS 5-Year Data Profiles
initialurl = "https://api.census.gov/data/{}/acs/{}/profile?get=NAME,group({})&for={}:{}&key={}".format(str(year), 'acs5', 'DP02', geography,'*',CENSUS_KEY)
acs_initial = requests.get(initialurl)
acs5_1 = json.loads(acs_initial.text)
acs5_data = pd.DataFrame(acs5_1[1:],columns=acs5_1[0])

for i in profiles:
    acs_year = str(year)
    acs_type = "acs5"
    acs_var = i
    acs_geolevel = geography
    acs_geo = "*"
    key = "54690f8093283c11c9612c58bc15b56ba3a26373"
    
    url = "https://api.census.gov/data/{}/acs/{}/profile?get=NAME,group({})&for={}:{}&key={}".format(acs_year, acs_type, acs_var, acs_geolevel, acs_geo,key)
    acs_five = requests.get(url)
    statcheck = acs_five.status_code
    
    if statcheck == 200:
        acs5_county = json.loads(acs_five.text)
        df1 = pd.DataFrame(acs5_county[1:],columns=acs5_county[0])
        acs5_data = acs5_data.merge(df1, on='GEO_ID', how = 'left')
    
    else:
        print('ERROR: '+statcheck)

dash_data = acs5_data[acs_variable_list]
dash_data = dash_data.loc[:,~dash_data.columns.duplicated()]
acs_columns = ['GEO_ID','NAME','state','place']
for i in variable_names:
    acs_columns.extend(i)
dash_data.columns = acs_columns
dash_data = dash_data.apply(pd.to_numeric,errors = 'ignore')

#Headline Table Calcs
dash_data['Homeowner Vacancy Rate'] = dash_data['Homeowner Vacancy Rate']/100
dash_data['Rental Vacancy Rate'] = dash_data['Rental Vacancy Rate']/100
dash_data['Homeownership Rate'] = dash_data['Owner Occupied Units']/(dash_data['Owner Occupied Units']+dash_data['Renter Occupied Units'])
dash_data['Rental Rate'] = 1-dash_data['Homeownership Rate']

#Unit Age Calcs
dash_data['Units Built 2010 and Later'] = dash_data['Units Built 2014 and Later']+dash_data['Units Built Between 2010 and 2013']

#Household Asssistance Calcs
dash_data['% of Households on Social Security'] = dash_data['Households Receiving Social Security']/dash_data['Total Households (HH Assistance)']
dash_data['% of Households Receiving Retirement Income'] = dash_data['Households Receiveing Retirement Income']/dash_data['Total Households (HH Assistance)']
dash_data['% of Households Receiving SSI'] = dash_data['Households Receiving SSI']/dash_data['Total Households (HH Assistance)']
dash_data['% of Households Receiving Cash Assistance'] = dash_data['Households Receiving Cash Assistance']/dash_data['Total Households (HH Assistance)']
dash_data['% of Households Receiving SNAP Benefits'] = dash_data['Households Receiving SNAP Benefits']/dash_data['Total Households (HH Assistance)']

#Special Populations Calcs
dash_data['% of Single Parent Househods'] = (dash_data['Single Male Parent Household']+dash_data['Single Female Parent Household'])/dash_data['Total Households']
dash_data['% of Inidividuals with a Disability'] = dash_data['Total Civilian Population with a Disability']/dash_data['Total Civilian Population']
dash_data['% of Inidividuals 65 or Older with a Disability'] = dash_data['Civilian Population 65 year and Older with a Disability']/dash_data['Civilian Population 65 year and Older']
dash_data['% of Non-Fluent English Speakers'] = dash_data['Population 5 years and Older who speak English less than very well']/dash_data['Population 5 years and Older']



#CHAS DATA Pull (NEED TO PUT CHAS DATA IN CHAS PATH)
#Pull in Files
place_chas_url = 'https://www.huduser.gov/portal/datasets/cp/'+str(chas_year-4)+'thru'+str(chas_year)+'-160-csv.zip'
r = requests.get(place_chas_url)
buf1 = io.BytesIO(r.content)

with zipfile.ZipFile(buf1, "r") as f:
    with f.open('2016thru2020-160-csv/Table17A.csv') as zd:
        seventeena = pd.read_csv(zd, encoding='latin-1')
    with f.open('2016thru2020-160-csv/Table17B.csv') as zd:
        seventeenb = pd.read_csv(zd, encoding='latin-1')
    with f.open('2016thru2020-160-csv/Table18A.csv') as zd:
        eighteena = pd.read_csv(zd, encoding='latin-1')
    with f.open('2016thru2020-160-csv/Table18B.csv') as zd:
        eighteenb = pd.read_csv(zd, encoding='latin-1')
    with f.open('2016thru2020-160-csv/Table18C.csv') as zd:
        eighteenc = pd.read_csv(zd, encoding='latin-1')

with zipfile.ZipFile(buf1, "r") as f:
    with f.open('CHAS-data-dictionary-16-20.xlsx') as zd:
        datadic17a = pd.read_excel(zd, sheet_name = 'Table 17A')
    with f.open('CHAS-data-dictionary-16-20.xlsx') as zd:
        datadic17b = pd.read_excel(zd, sheet_name = 'Table 17B')
    with f.open('CHAS-data-dictionary-16-20.xlsx') as zd:
        datadic18a = pd.read_excel(zd, sheet_name = 'Table 18A')
    with f.open('CHAS-data-dictionary-16-20.xlsx') as zd:
        datadic18b = pd.read_excel(zd, sheet_name = 'Table 18B')
    with f.open('CHAS-data-dictionary-16-20.xlsx') as zd:
        datadic18c = pd.read_excel(zd, sheet_name = 'Table 18C')

#Renter/Owner Compilation

#Renter Owner Identification
test1 = datadic18c[datadic18c['Household income'] == 'less than or equal to 30% of HAMFI']
rentersless30 = test1['Column Name'].tolist()

test1 = datadic18c[datadic18c['Household income'] == 'greater than 30% of HAMFI but less than or equal to 50% of HAMFI']
renters3050 = test1['Column Name'].tolist()

test1 = datadic18c[datadic18c['Household income'] == 'greater than 50% of HAMFI but less than or equal to 80% of HAMFI']
renters5080 = test1['Column Name'].tolist()

test1 = datadic18c[datadic18c['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI']
renters80100 = test1['Column Name'].tolist()

test1 = datadic18c[datadic18c['Household income'] == 'greater than 100% of HAMFI']
renters100up = test1['Column Name'].tolist()

test1 = datadic18a[datadic18a['Household income'] == 'less than or equal to 30% of HAMFI']
ownersless30 = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Household income'] == 'less than or equal to 30% of HAMFI']
ownersless30b = test1['Column Name'].tolist()
ownersless30.extend(ownersless30b)

test1 = datadic18a[datadic18a['Household income'] == 'greater than 30% of HAMFI but less than or equal to 50% of HAMFI']
owners3050 = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Household income'] == 'greater than 30% of HAMFI but less than or equal to 50% of HAMFI']
owners3050b = test1['Column Name'].tolist()
owners3050.extend(owners3050b)

test1 = datadic18a[datadic18a['Household income'] == 'greater than 50% of HAMFI but less than or equal to 80% of HAMFI']
owners5080 = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Household income'] == 'greater than 50% of HAMFI but less than or equal to 80% of HAMFI']
owners5080b = test1['Column Name'].tolist()
owners5080.extend(owners5080b)

test1 = datadic18a[datadic18a['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI']
owners80100 = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI']
owners80100b = test1['Column Name'].tolist()
owners80100.extend(owners5080b)

test1 = datadic18a[datadic18a['Household income'] == 'greater than 100% of HAMFI']
owners100up = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Household income'] == 'greater than 100% of HAMFI']
owners100upb = test1['Column Name'].tolist()
owners100up.extend(owners100upb)


#Renter Owner Summation
gap_data = seventeena
gap_data = gap_data.merge(seventeenb, on='geoid', how='left')
gap_data = gap_data.merge(eighteena, on='geoid', how='left')
gap_data = gap_data.merge(eighteenb, on='geoid', how='left')
gap_data = gap_data.merge(eighteenc, on='geoid', how='left')

gap_data['rentersless30'] = gap_data[rentersless30].sum(axis=1)
gap_data['renters3050'] = gap_data[renters3050].sum(axis=1)
gap_data['renters5080'] = gap_data[renters5080].sum(axis=1)
gap_data['renters80100'] = gap_data[renters80100].sum(axis=1)
gap_data['renters100up'] = gap_data[renters100up].sum(axis=1)

gap_data['ownersless30'] = gap_data[ownersless30].sum(axis=1)
gap_data['owners3050'] = gap_data[owners3050].sum(axis=1)
gap_data['owners5080'] = gap_data[owners5080].sum(axis=1)
gap_data['owners80100'] = gap_data[owners80100].sum(axis=1)
gap_data['owners100up'] = gap_data[owners100up].sum(axis=1)

#Rental/Owner Units

#Identification
test1 = datadic18c[datadic18c['Rent'] == 'less than or equal to RHUD30']
test1 = test1[test1['Household income'] == 'All']
runitsless30 = test1['Column Name'].tolist()
test1 = datadic17b[datadic17b['Rent'] == 'less than or equal to RHUD30']
runitsless30v = test1['Column Name'].tolist()
runitsless30.extend(runitsless30v)

test1 = datadic18c[datadic18c['Rent']  == 'greater than RHUD30 and less than or equal to RHUD50']
test1 = test1[test1['Household income'] == 'All']
runits3050 = test1['Column Name'].tolist()
test1 = datadic17b[datadic17b['Rent'] == 'greater than RHUD30 and less than or equal to RHUD50']
runits3050v = test1['Column Name'].tolist()
runits3050.extend(runits3050v)

test1 = datadic18c[datadic18c['Rent']  == 'greater than RHUD50 and less than or equal to RHUD80']
test1 = test1[test1['Household income'] == 'All']
runits5080 = test1['Column Name'].tolist()
test1 = datadic17b[datadic17b['Rent'] == 'greater than RHUD50 and less than or equal to RHUD80']
runits5080v = test1['Column Name'].tolist()
runits5080.extend(runits5080v)

test1 = datadic18c[datadic18c['Rent'] == 'greater than RHUD80']
test1 = test1[test1['Household income'] == 'All']
runits80up = test1['Column Name'].tolist()
test1 = datadic17b[datadic17b['Rent'] == 'greater than RHUD80']
runits80upv = test1['Column Name'].tolist()
runits80up.extend(runits80upv)


test1 = datadic18a[datadic18a['Home value'] == 'Value less than or equal to VHUD50']
test1 = test1[test1['Household income'] == 'All']
ounitsless50 = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Home value'] == 'Value less than or equal to VHUD50']
test1 = test1[test1['Household income'] == 'All']
ounitsless50b = test1['Column Name'].tolist()
ounitsless50.extend(ounitsless50b)
test1 = datadic17a[datadic17a['Asking price'] == 'Value less than or equal to VHUD50']
ounitsless50v = test1['Column Name'].tolist()
ounitsless50.extend(ounitsless50v)

test1 = datadic18a[datadic18a['Home value'] == 'Value greater than VHUD50 and less than or equal to VHUD80']
test1 = test1[test1['Household income'] == 'All']
ounits5080 = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Home value'] == 'Value greater than VHUD50 and less than or equal to VHUD80']
test1 = test1[test1['Household income'] == 'All']
ounits5080b = test1['Column Name'].tolist()
ounits5080.extend(ounits5080b)
test1 = datadic17a[datadic17a['Asking price'] == 'Value greater than VHUD50 and less than or equal to VHUD80']
ounits5080v = test1['Column Name'].tolist()
ounits5080.extend(ounits5080v)

test1 = datadic18a[datadic18a['Home value'] == 'Value greater than VHUD80 and less than or equal to VHUD100']
test1 = test1[test1['Household income'] == 'All']
ounits80100 = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Home value'] == 'Value greater than VHUD80 and less than or equal to VHUD100']
test1 = test1[test1['Household income'] == 'All']
ounits80100b = test1['Column Name'].tolist()
ounits80100.extend(ounits80100b)
test1 = datadic17a[datadic17a['Asking price'] == 'Value greater than VHUD80 and less than or equal to VHUD100']
ounits80100v = test1['Column Name'].tolist()
ounits80100.extend(ounits80100v)

test1 = datadic18a[datadic18a['Home value'] == 'Value greater than VHUD100']
test1 = test1[test1['Household income'] == 'All']
ounits100up = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Home value'] == 'Value greater than VHUD100']
test1 = test1[test1['Household income'] == 'All']
ounits100upb = test1['Column Name'].tolist()
ounits100up.extend(ounits100upb)
test1 = datadic17a[datadic17a['Asking price'] == 'Value greater than VHUD100']
ounits100upv = test1['Column Name'].tolist()
ounits100up.extend(ounits100upv)

gap_data['runitsless30'] = gap_data[runitsless30].sum(axis=1)
gap_data['runits3050'] = gap_data[runits3050].sum(axis=1)
gap_data['runits5080'] = gap_data[runits5080].sum(axis=1)
gap_data['runits80up'] = gap_data[runits80up].sum(axis=1)


gap_data['ounitsless50'] = gap_data[ounitsless50].sum(axis=1)
gap_data['ounits5080'] = gap_data[ounits5080].sum(axis=1)
gap_data['ounits80100'] = gap_data[ounits80100].sum(axis=1)
gap_data['ounits100up'] = gap_data[ounits100up].sum(axis=1)

#Units Occupied By High Income Group

#Identification
test1 = datadic18c[datadic18c['Rent'] == 'less than or equal to RHUD30']
test1 = test1[(test1['Household income'] == 'greater than 30% of HAMFI but less than or equal to 50% of HAMFI') | (test1['Household income'] == 'greater than 50% of HAMFI but less than or equal to 80% of HAMFI') | 
              (test1['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI') | (test1['Household income'] == 'greater than 100% of HAMFI')]
rless30hhabove = test1['Column Name'].tolist()

test1 = datadic18c[datadic18c['Rent'] == 'greater than RHUD30 and less than or equal to RHUD50']
test1 = test1[(test1['Household income'] == 'greater than 50% of HAMFI but less than or equal to 80% of HAMFI') | 
              (test1['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI') | (test1['Household income'] == 'greater than 100% of HAMFI')]
r3050hhabove = test1['Column Name'].tolist()

test1 = datadic18c[datadic18c['Rent'] == 'greater than RHUD50 and less than or equal to RHUD80']
test1 = test1[ (test1['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI') | (test1['Household income'] == 'greater than 100% of HAMFI')]
r5080hhabove = test1['Column Name'].tolist()


test1 = datadic18a[datadic18a['Home value'] == 'Value less than or equal to VHUD50']
test1 = test1[(test1['Household income'] == 'greater than 50% of HAMFI but less than or equal to 80% of HAMFI') | 
              (test1['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI') | (test1['Household income'] == 'greater than 100% of HAMFI')]
hless50hhabove = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Home value'] == 'Value less than or equal to VHUD50']
test1 = test1[(test1['Household income'] == 'greater than 50% of HAMFI but less than or equal to 80% of HAMFI') | 
              (test1['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI') | (test1['Household income'] == 'greater than 100% of HAMFI')]
hless50hhaboveb = test1['Column Name'].tolist()
hless50hhabove.extend(hless50hhaboveb)

test1 = datadic18a[datadic18a['Home value'] == 'Value greater than VHUD50 and less than or equal to VHUD80']
test1 = test1[(test1['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI') | (test1['Household income'] == 'greater than 100% of HAMFI')]
h5080hhabove = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Home value'] == 'Value greater than VHUD50 and less than or equal to VHUD80']
test1 = test1[(test1['Household income'] == 'greater than 80% of HAMFI but less than or equal to 100% of HAMFI') | (test1['Household income'] == 'greater than 100% of HAMFI')]
h5080hhaboveb = test1['Column Name'].tolist()
h5080hhabove.extend(h5080hhaboveb)

test1 = datadic18a[datadic18a['Home value'] == 'Value greater than VHUD80 and less than or equal to VHUD100']
test1 = test1[test1['Household income'] == 'greater than 100% of HAMFI']
h80100hhabove = test1['Column Name'].tolist()
test1 = datadic18b[datadic18b['Home value'] == 'Value greater than VHUD80 and less than or equal to VHUD100']
test1 = test1[test1['Household income'] == 'greater than 100% of HAMFI']
h80100hhaboveb = test1['Column Name'].tolist()
h80100hhabove.extend(h80100hhaboveb)

gap_data['rless30hhabove'] = gap_data[rless30hhabove].sum(axis=1)
gap_data['r3050hhabove'] = gap_data[r3050hhabove].sum(axis=1)
gap_data['r5080hhabove'] = gap_data[r5080hhabove].sum(axis=1)


gap_data['oless50hhabove'] = gap_data[hless50hhabove].sum(axis=1)
gap_data['o5080hhabove'] = gap_data[h5080hhabove].sum(axis=1)
gap_data['o80100hhabove'] = gap_data[h80100hhabove].sum(axis=1)


#Clean Dataframe
gap_data = gap_data[['geoid','name_x','place_x','rentersless30','renters3050','renters5080','renters80100','renters100up',
                   'ownersless30','owners3050','owners5080','owners80100','owners100up','runitsless30','runits3050','runits5080',
                   'runits80up','ounitsless50','ounits5080','ounits80100','ounits100up', 'rless30hhabove', 'r3050hhabove', 'r5080hhabove',
                    'oless50hhabove', 'o5080hhabove', 'o80100hhabove']]

gapcolumns = ['GEO_ID','name','place','rentersless30','renters3050','renters5080','renters80100','renters100up',
                   'ownersless30','owners3050','owners5080','owners80100','owners100up','runitsless30','runits3050','runits5080',
                   'runits80up','ounitsless50','ounits5080','ounits80100','ounits100up', 'rless30hhabove', 'r3050hhabove', 'r5080hhabove',
                    'oless50hhabove', 'o5080hhabove', 'o80100hhabove']

gap_data = gap_data.loc[:,~gap_data.columns.duplicated()]
gap_data.columns = gapcolumns

gap_data = gap_data[['GEO_ID','name','rentersless30','renters3050','renters5080','renters80100','renters100up',
                   'ownersless30','owners3050','owners5080','owners80100','owners100up','runitsless30','runits3050','runits5080',
                   'runits80up','ounitsless50','ounits5080','ounits80100','ounits100up', 'rless30hhabove', 'r3050hhabove', 'r5080hhabove',
                    'oless50hhabove', 'o5080hhabove', 'o80100hhabove']]

#Calculations
gap_data['grossless30rentgap'] = gap_data['runitsless30']-gap_data['rentersless30']
gap_data['gross3050rentgap'] = gap_data['runits3050']-gap_data['renters3050']
gap_data['gross5080rentgap'] = gap_data['runits5080']-gap_data['renters5080']
gap_data['gross80uprentgap'] = gap_data['runits80up']-(gap_data['renters80100']+gap_data['renters100up'])

gap_data['grossless50owngap'] = gap_data['ounitsless50']-(gap_data['ownersless30']+gap_data['owners3050'])
gap_data['gross5080owngap'] = gap_data['ounits5080']-gap_data['owners5080']
gap_data['gross80100owngap'] = gap_data['ounits80100']-gap_data['owners80100']
gap_data['gross100upowngap'] = gap_data['ounits100up']-gap_data['owners100up']


gap_data['netless30rentgap'] = (gap_data['runitsless30']-gap_data['rless30hhabove'])-gap_data['rentersless30']
gap_data['net3050rentgap'] = (gap_data['runits3050']-gap_data['r3050hhabove'])-gap_data['renters3050']
gap_data['net5080rentgap'] = (gap_data['runits5080']-gap_data['r5080hhabove'])-gap_data['renters5080']
gap_data['net80uprentgap'] = gap_data['gross80uprentgap']

gap_data['netless50owngap'] = (gap_data['ounitsless50']-gap_data['oless50hhabove'])-(gap_data['ownersless30']+gap_data['owners3050'])
gap_data['net5080owngap'] = (gap_data['ounits5080']-gap_data['o5080hhabove'])-gap_data['owners5080']
gap_data['net80100owngap'] = (gap_data['ounits80100']-gap_data['o80100hhabove'])-gap_data['owners80100']
gap_data['net100upowngap'] = gap_data['gross100upowngap']

gap_data['GEO_ID'] = gap_data['GEO_ID'].apply(lambda x: x[:2] + '00' + x[2:])
gap_data['testid'] = gap_data.GEO_ID.str.split("US").str.get(-1)
gap_data['GEO_ID'] = '1600000US' + gap_data['testid']
dash_data = dash_data.merge(gap_data,on='GEO_ID',how='left')

#Household Size Data Pull
s2501url = "https://api.census.gov/data/{}/acs/{}/subject?get=NAME,group({})&for={}:{}&key={}".format(str(year), 'acs5', 'S2501', geography,'*',CENSUS_KEY)
s2501_i = requests.get(s2501url)
s2501_txt = json.loads(s2501_i.text)
s2501 = pd.DataFrame(s2501_txt[1:],columns=s2501_txt[0])

s2501_change = ['GEO_ID']
s2501_change.extend(hhsize_variables)
s2501_cols = ['GEO_ID']
s2501_cols.extend(hhsize_var_names)

s2501 = s2501[s2501_change]
s2501.columns = s2501_cols
dash_data = dash_data.merge(s2501,on='GEO_ID',how='left')


#Population Tree Data Pull
#ACS API Pull
whitepopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001H)&for={}:{}".format(str(year),censuskey,geography,geotype)
blackpopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001B)&for={}:{}".format(str(year),censuskey,geography,geotype)
nativepopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001C)&for={}:{}".format(str(year),censuskey,geography,geotype)
asianpopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001D)&for={}:{}".format(str(year),censuskey,geography,geotype)
pacificpopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001E)&for={}:{}".format(str(year),censuskey,geography,geotype)
otherpopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001F)&for={}:{}".format(str(year),censuskey,geography,geotype)
multipopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001G)&for={}:{}".format(str(year),censuskey,geography,geotype)
latinpopurl = "https://api.census.gov/data/{}/acs/acs5?key={}&get=NAME,group(B01001I)&for={}:{}".format(str(year),censuskey,geography,geotype)
whitepoprequests = requests.get(whitepopurl)
blackpoprequests = requests.get(blackpopurl)
nativepoprequests = requests.get(nativepopurl)
asianpoprequests = requests.get(asianpopurl)
pacificpoprequests = requests.get(pacificpopurl)
otherpoprequests = requests.get(otherpopurl)
multipoprequests = requests.get(multipopurl)
latinpoprequests = requests.get(latinpopurl)
whitetxt = json.loads(whitepoprequests.text)
blacktxt = json.loads(blackpoprequests.text)
nativetxt = json.loads(nativepoprequests.text)
asiantxt = json.loads(asianpoprequests.text)
pacifictxt = json.loads(pacificpoprequests.text)
othertxt = json.loads(otherpoprequests.text)
multitxt = json.loads(multipoprequests.text)
latintxt = json.loads(latinpoprequests.text)
whitedf = pd.DataFrame(whitetxt[1:],columns=whitetxt[0])
blackdf = pd.DataFrame(blacktxt[1:],columns=blacktxt[0]) 
nativedf = pd.DataFrame(nativetxt[1:],columns=nativetxt[0])
asiandf = pd.DataFrame(asiantxt[1:],columns=asiantxt[0])
pacificdf = pd.DataFrame(pacifictxt[1:],columns=pacifictxt[0])
otherdf = pd.DataFrame(othertxt[1:],columns=othertxt[0])
multidf = pd.DataFrame(multitxt[1:],columns=multitxt[0])
latindf = pd.DataFrame(latintxt[1:],columns=latintxt[0])
whitedf = whitedf[whitepop_variables]
blackdf = blackdf[blackpop_variables]
nativedf = nativedf[nativepop_variables]
asiandf = asiandf[asianpop_variables]
pacificdf = pacificdf[pacificpop_variables]
otherdf = otherdf[otherpop_variables]
multidf = multidf[multipop_variables]
latindf = latindf[latinpop_variables]
whitedf.columns = whitepop_var_names
blackdf.columns = blackpop_var_names
nativedf.columns = nativepop_var_names
asiandf.columns = asianpop_var_names
pacificdf.columns = pacificpop_var_names
otherdf.columns = otherpop_var_names
multidf.columns = multipop_var_names
latindf.columns = latinpop_var_names
whitedf = whitedf.apply(pd.to_numeric,errors='ignore')
blackdf = blackdf.apply(pd.to_numeric,errors='ignore')
nativedf = nativedf.apply(pd.to_numeric,errors='ignore')
asiandf = asiandf.apply(pd.to_numeric,errors='ignore')
pacificdf = pacificdf.apply(pd.to_numeric,errors='ignore')
otherdf = otherdf.apply(pd.to_numeric,errors='ignore')
multidf = multidf.apply(pd.to_numeric,errors='ignore')
latindf = latindf.apply(pd.to_numeric,errors='ignore')

#Total Pop Calculation
whitedf['White Population'] = whitedf.drop('GEO_ID', axis=1).sum(axis=1)
blackdf['Black Population'] = blackdf.drop('GEO_ID', axis=1).sum(axis=1)
nativedf['Native American Population'] = nativedf.drop('GEO_ID', axis=1).sum(axis=1)
asiandf['Asian Population'] = asiandf.drop('GEO_ID', axis=1).sum(axis=1)
pacificdf['Hawaiian or Pacific Islander Population'] = pacificdf.drop('GEO_ID', axis=1).sum(axis=1)
otherdf['Other Race Population'] = otherdf.drop('GEO_ID', axis=1).sum(axis=1)
multidf['Multiracial Population'] = multidf.drop('GEO_ID', axis=1).sum(axis=1)
latindf['Latinx Population'] = latindf.drop('GEO_ID', axis=1).sum(axis=1)

#Teenage Pop Calculation
whitedf['White Male 15-19 years'] = whitedf.iloc[:,[4,5]].sum(axis=1)
blackdf['Black Male 15-19 years'] = blackdf.iloc[:,[4,5]].sum(axis=1)
nativedf['Native American Male 15-19 years'] = nativedf.iloc[:,[4,5]].sum(axis=1)
asiandf['Asian Male 15-19 years'] = asiandf.iloc[:,[4,5]].sum(axis=1)
pacificdf['Hawaiian or Pacific Islander Male 15-19 years'] = pacificdf.iloc[:,[4,5]].sum(axis=1)
otherdf['Other Male 15-19 years'] = otherdf.iloc[:,[4,5]].sum(axis=1)
multidf['Multiracial Male 15-19 years'] = multidf.iloc[:,[4,5]].sum(axis=1)
latindf['Latinx Male 15-19 years'] = latindf.iloc[:,[4,5]].sum(axis=1)

whitedf['White Female 15-19 years'] = whitedf.iloc[:,[18,19]].sum(axis=1)
blackdf['Black Female 15-19 years'] = blackdf.iloc[:,[4,5]].sum(axis=1)
nativedf['Native American Female 15-19 years'] = nativedf.iloc[:,[4,5]].sum(axis=1)
asiandf['Asian Female 15-19 years'] = asiandf.iloc[:,[4,5]].sum(axis=1)
pacificdf['Hawaiian or Pacific Islander Female 15-19 years'] = pacificdf.iloc[:,[4,5]].sum(axis=1)
otherdf['Other Female 15-19 years'] = otherdf.iloc[:,[4,5]].sum(axis=1)
multidf['Multiracial Female 15-19 years'] = multidf.iloc[:,[4,5]].sum(axis=1)
latindf['Latinx Female 15-19 years'] = latindf.iloc[:,[4,5]].sum(axis=1)

#Merge Together
poptable = whitedf
poptable = poptable.merge(blackdf,on='GEO_ID',how='left')
poptable = poptable.merge(nativedf,on='GEO_ID',how='left')
poptable = poptable.merge(asiandf,on='GEO_ID',how='left')
poptable = poptable.merge(pacificdf,on='GEO_ID',how='left')
poptable = poptable.merge(otherdf,on='GEO_ID',how='left')
poptable = poptable.merge(multidf,on='GEO_ID',how='left')
poptable = poptable.merge(latindf,on='GEO_ID',how='left')

#Pop Tree Variables
poptable['Male 0-4 years'] = poptable[malepop0to4].sum(axis=1)
poptable['Male 5-9 years'] = poptable[malepop5to9].sum(axis=1)
poptable['Male 10-14 years'] = poptable[malepop10to14].sum(axis=1)
poptable['Male 15-19 years'] = poptable[malepop15to19].sum(axis=1)
poptable['Male 20-24 years'] = poptable[malepop20to24].sum(axis=1)
poptable['Male 25-29 years'] = poptable[malepop25to29].sum(axis=1)
poptable['Male 30-34 years'] = poptable[malepop30to34].sum(axis=1)
poptable['Male 35-44 years'] = poptable[malepop35to44].sum(axis=1)
poptable['Male 45-54 years'] = poptable[malepop45to54].sum(axis=1)
poptable['Male 55-64 years'] = poptable[malepop55to64].sum(axis=1)
poptable['Male 65-74 years'] = poptable[malepop65to74].sum(axis=1)
poptable['Male 75-84 years'] = poptable[malepop75to84].sum(axis=1)
poptable['Male 85 years +'] = poptable[malepop85up].sum(axis=1)
poptable['Female 0-4 years'] = poptable[femalepop0to4].sum(axis=1)
poptable['Female 5-9 years'] = poptable[femalepop5to9].sum(axis=1)
poptable['Female 10-14 years'] = poptable[femalepop10to14].sum(axis=1)
poptable['Female 15-19 years'] = poptable[femalepop15to19].sum(axis=1)
poptable['Female 20-24 years'] = poptable[femalepop20to24].sum(axis=1)
poptable['Female 25-29 years'] = poptable[femalepop25to29].sum(axis=1)
poptable['Female 30-34 years'] = poptable[femalepop30to34].sum(axis=1)
poptable['Female 35-44 years'] = poptable[femalepop35to44].sum(axis=1)
poptable['Female 45-54 years'] = poptable[femalepop45to54].sum(axis=1)
poptable['Female 55-64 years'] = poptable[femalepop55to64].sum(axis=1)
poptable['Female 65-74 years'] = poptable[femalepop65to74].sum(axis=1)
poptable['Female 75-84 years'] = poptable[femalepop75to84].sum(axis=1)
poptable['Female 85 years +'] = poptable[femalepop85up].sum(axis=1)

#Combine with Dash_data
merge_variables = ['GEO_ID']
merge_variables.extend(malepoplist)
merge_variables.extend(femalepoplist)
merge_variables.extend(racepoptotals)
pop_variables = poptable[merge_variables]
dash_data = dash_data.merge(pop_variables,on='GEO_ID',how='left')

#Assisted Units
#Data Sources
multifamily_assisted = esri_import('https://services.arcgis.com/VTyQ9soqVukalItT/ArcGIS/rest/services/MULTIFAMILY_PROPERTIES_ASSISTED/FeatureServer/13')
public_housing = esri_import('https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/Public_Housing_Buildings/FeatureServer/10')
lihtc_housing = esri_import('https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/LIHTC/FeatureServer/11')
try:
    initial_url = 'https://www.huduser.gov/portal/datasets/pictures/files/COUNTY_{}.xlsx'.format(year_minus1)
    county_HUD_picture = pd.read_excel(initial_url)
except:
    next_url = 'https://www.huduser.gov/portal/datasets/pictures/files/COUNTY_{}.xlsx'.format(year_minus2)
    county_HUD_picture = pd.read_excel(next_url)


#Wrangling
mf_assisted = multifamily_assisted[['PROPERTY_ID', 'UGLG_KEY','PROPERTY_NAME_TEXT','TOTAL_ASSISTED_UNIT_COUNT', 'TOTAL_UNIT_COUNT', 
                                    'PROPERTY_CATEGORY_NAME', 'CLIENT_GROUP_CODE', 'CLIENT_GROUP_NAME', 'CLIENT_GROUP_TYPE', 'HAS_ACTIVE_FINANCING_IND', 'PRIMARY_FINANCING_TYPE', 
                                    'HAS_SERVICE_AGREEMENT_IND', 'HAS_USE_RESTRICTION_IND', 'HAS_ACTIVE_IRP_IND', 'TROUBLED_CODE', 'OPIIS_RISK_CATEGORY', 'IS_INSURED_IND', 'WAS_EVER_INSURED_IND', 
                                    'IS_202_811_IND', 'WAS_EVER_202_811_IND', 'IS_HUD_HELD_IND', 'IS_HUD_OWNED_IND', 'IS_FLEXIBLE_SUBSIDY_IND', 'IS_HOSPITAL_IND', 'IS_NURSING_HOME_IND', 
                                    'IS_BOARD_AND_CARE_IND', 'IS_ASSISTED_LIVING_IND', 'IS_REFINANCED_IND', 'IS_221D3_IND', 'IS_221D4_IND', 'IS_236_IND', 'IS_IN_DEFAULT_DELINQUENT_IND', 
                                    'IS_NON_INSURED_IND', 'IS_BMIR_IND', 'IS_RISK_SHARING_IND', 'IS_MIP_IND', 'IS_CO_INSURED_IND', 'IS_SUBSIDIZED_IND', 'IS_SEC8_IND', 'IS_PAC_IND', 'IS_PRAC_IND', 
                                    'IS_RENT_SUPPLEMENT_IND', 'IS_SECTION_236_RAP_IND', 'IS_SEC8_202_IND', 'IS_SEC8_FMHA_515_IND', 'IS_SEC8_LMSA_IND', 'IS_SEC8_PRPRTY_DISPOSITION_IND', 
                                    'IS_SEC8_PRESERVATION_IND', 'IS_SEC8_OTHR_NW_CNSTRCTION_IND', 'IS_SEC8_OTHER_SUB_REHAB_IND', 'IS_PENSION_FUND_IND', 'IS_PRAC_811_IND', 'IS_GREEN_RETROFIT_IND', 
                                    'IS_202_DIRECT_LOAN_IND', 'IS_202_CAPITAL_ADVANCE_IND', 'IS_811_CAPITAL_ADVANCE_IND', 'ENERGY_PERFORMANCE_CONTRCT_IND', 'IS_SEC8_RAD_DEMO_CONV_IND', 
                                    'UNITS1', 'UNITS2', 'MAXIMUM_CONTRACT_UNIT_COUNT', 'PROGRAM_TYPE1', 'PROGRAM_TYPE2', 'EXPIRATION_DATE1', 'EXPIRATION_DATE2', 'RENT_TO_FMR_RATIO1', 'RENT_TO_FMR_RATIO2', 
                                    'BD0_CNT1', 'BD0_CNT2', 'BD1_CNT1', 'BD1_CNT2', 'BD2_CNT1', 'BD2_CNT2', 'BD3_CNT1', 'BD3_CNT2', 'BD4_CNT1', 'BD4_CNT2', 'BD5_CNT1', 'BD5_CNT2', 'TAXCREDIT1', 'TAXCREDIT2',
                                    'STATE2KX', 'CNTY_NM2KX', 'CNTY2KX', 'TRACT2KX', 'CURCNTY_NM', 'CURCNTY', 'CURCOSUB', 'CURCOSUB_NM', 'PLACE2KX', 'PLACE_NM2KX', 'PLACE_CC2KX', 'PLACE_INC2KX', 
                                    'MSA', 'MSA_NM', 'CBSA', 'CBSA_NM', 'STD_ST', 'STD_ZIP5', 'STD_ZIP9', 'ZIP_CLASS', 'COUNTY_LEVEL', 'PLACE_LEVEL', 'TRACT_LEVEL', 'BLKGRP_LEVEL',
                                    'FASS_LAST_REPORTING_END_DT', 'FULL_DEBT_RESTRUCTURE_DATE', 'LAST_CRITICAL_DATE', 'NGHBRHD_NTWRK_EST_DATE', 'ORIGINAL_LOAN_AMOUNT', 'UNIT_MRKT_RENT_CNT',
                                    'TOTAL_AVBL_UNITS', 'PCT_OCCUPIED', 'NUMBER_REPORTED', 'PEOPLE_PER_UNIT', 'PEOPLE_TOTAL', 'RENT_PER_MONTH', 'SPENDING_PER_MONTH', 'HH_INCOME', 'OCCUPANCY_DATE',
                                    'geometry']]
mf_assisted = mf_assisted.drop_duplicates(subset = ['PROPERTY_ID'])
mf_assisted_units = mf_assisted[['PROPERTY_ID', 'PROPERTY_NAME_TEXT','TOTAL_ASSISTED_UNIT_COUNT', 'TOTAL_UNIT_COUNT','HAS_ACTIVE_FINANCING_IND', 'PRIMARY_FINANCING_TYPE', 'PROGRAM_TYPE1', 'PROGRAM_TYPE2', 
                                 'EXPIRATION_DATE1', 'EXPIRATION_DATE2', 'BD0_CNT1', 'BD0_CNT2', 'BD1_CNT1', 'BD1_CNT2', 'BD2_CNT1', 'BD2_CNT2', 'BD3_CNT1', 'BD3_CNT2', 'BD4_CNT1', 'BD4_CNT2', 
                                 'MAXIMUM_CONTRACT_UNIT_COUNT', 'BD5_CNT1', 'BD5_CNT2','OCCUPANCY_DATE', 'COUNTY_LEVEL', 'PLACE_LEVEL']]

ifA = [mf_assisted_units['PROGRAM_TYPE1'].str.contains('202', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('811', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('542', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('MR', na=False),
        mf_assisted_units['PROGRAM_TYPE1'].str.contains('Mod Rehab', na=False),
        mf_assisted_units['PROGRAM_TYPE1'].str.contains('BMIR', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('SR', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('236', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('221', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('223', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('RAD', na=False),
       mf_assisted_units['PROGRAM_TYPE1'].str.contains('8', na=False),
      mf_assisted_units['PROGRAM_TYPE1'].str.contains('PRAC', na=False)]
thenA = ['202 - Elderly', '811 - Disabled', 'HUD Insured', 'Moderate Rehab', 'Moderate Rehab', 'Substantial Rehab', 'Substantial Rehab', '236/BMIR', 'Mortgage/Loans', 'Mortgage/Loans', 'RAD', 'Section 8', 'Section 8']

mf_assisted_units['Type'] =  np.select(ifA, thenA, default='Other Assisted')

pnames = list(mf_assisted_units.Type.unique())

#Calculations
place_assisted_units = mf_assisted_units[['MAXIMUM_CONTRACT_UNIT_COUNT', 'Type', 'PLACE_LEVEL']]
place_assisted_units = place_assisted_units.groupby(['PLACE_LEVEL', 'Type']).sum()
place_assisted_units = place_assisted_units.reset_index()

for i in pnames:
    temp_df = place_assisted_units[place_assisted_units['Type'] == i]
    temp_df = temp_df[['PLACE_LEVEL', 'MAXIMUM_CONTRACT_UNIT_COUNT']]
    temp_df.columns = ['PLACE_LEVEL', i]
    place_assisted_units = place_assisted_units.merge(temp_df, on='PLACE_LEVEL', how='left')
    place_assisted_units[i] = place_assisted_units[i].fillna(0)

place_assisted_units = place_assisted_units.drop(columns=['Type','MAXIMUM_CONTRACT_UNIT_COUNT'])
place_assisted_units = place_assisted_units.drop_duplicates(subset = 'PLACE_LEVEL')

plc_publichousing = public_housing[['PLACE_LEVEL', 'TOTAL_UNITS']]
plc_publichousing = plc_publichousing.groupby('PLACE_LEVEL').sum().reset_index()
plc_publichousing.columns = ['PLACE_LEVEL', 'Public Housing']
place_assisted_units = place_assisted_units.merge(plc_publichousing, on='PLACE_LEVEL', how='left')

plc_lihtc = lihtc_housing[['PLACE_LEVEL', 'LI_UNITS']]
plc_lihtc = plc_lihtc.groupby('PLACE_LEVEL').sum().reset_index()
plc_lihtc['PLACE_LEVEL'] =  plc_lihtc['PLACE_LEVEL'].apply(lambda x: '0' + x if len(x)<7 else x)
plc_lihtc.columns = ['PLACE_LEVEL', 'LIHTC']
place_assisted_units = place_assisted_units.merge(plc_lihtc, on='PLACE_LEVEL', how='left')

try:
    initial_url = 'https://www.huduser.gov/portal/datasets/pictures/files/PLACE_{}.xlsx'.format(year_minus1)
    place_HUD_picture = pd.read_excel(initial_url)
except:
    next_url = 'https://www.huduser.gov/portal/datasets/pictures/files/PLACE_{}.xlsx'.format(year_minus2)
    place_HUD_picture = pd.read_excel(next_url)


place_HUD_picture = place_HUD_picture[['program', 'code', 'total_units']]
place_HUD_picture = place_HUD_picture[place_HUD_picture['program']==3]
place_HUD_picture = place_HUD_picture[['code', 'total_units']]
place_HUD_picture.columns = ['PLACE_LEVEL', 'HCV Units']
place_assisted_units = place_assisted_units.merge(place_HUD_picture, on='PLACE_LEVEL', how='left')

place_assisted_units = place_assisted_units.fillna(0)


place_assisted_units['Assisted Units'] = place_assisted_units[['811 - Disabled', 'Other Assisted', '202 - Elderly', 'Section 8', 'Substantial Rehab', '236/BMIR', 
                                                             'RAD', 'Moderate Rehab', 'Mortgage/Loans', 'HUD Insured', 'Public Housing', 'LIHTC', 'HCV Units']].sum(axis=1)



#Combining And Saving
place_assisted_units['GEO_ID'] = place_assisted_units['PLACE_LEVEL'].apply(lambda x: '1600000US'+str(x))
place_assisted_units = place_assisted_units[['GEO_ID', '811 - Disabled', 'Other Assisted', '202 - Elderly', 'Section 8', 'Substantial Rehab', '236/BMIR', 
                                                             'RAD', 'Moderate Rehab', 'Mortgage/Loans', 'HUD Insured', 'Public Housing', 'LIHTC', 'HCV Units', 'Assisted Units']]

dash_data = dash_data.merge(place_assisted_units, on='GEO_ID', how='left')



dash_data.to_csv(str(base_path /"pdashdata.csv"))

#Dataframe for Download Transformations
data = dash_data
data = data.transpose()

data = data.reset_index()
pos = [2,3]
data.drop(data.index[pos], inplace=True)

new_header = data.iloc[1] 
data.drop(data.index[1], inplace=True)
data.columns = new_header 

cols = list(data.columns)
cols = cols[1:]
cols.insert(0, 'Variable')
data.columns = cols
data = data.apply(pd.to_numeric,errors = 'ignore')

data.to_csv(str(base_path /"pcsvdownload.csv"))

print('UPDATE COMPLETE! SAVED TO '+str(save_path))




