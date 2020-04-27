from pathlib import Path
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlite3
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

path = Path(__file__).resolve().parent.parent / "data" / "wine_data.sqlite"
conn = sqlite3.connect(str(path))
c = conn.cursor()

df = pd.read_sql("select * from wine_data", conn)

df = df[['country','description','rating','price','province','title','variety','winery','color','varietyID']]
#This is a test