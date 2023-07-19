import math
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import requests
import random
from datetime import datetime
import openpyxl   #para leer los excels
from bs4 import BeautifulSoup
import yfinance as yf



def getSymbols(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    ipc_table = pd.read_html(str(table))[0]
    # extraemos símbolos
    stocks = []
    for row in ipc_table.Symbol:
        symbol = row.strip().replace(" ", "").replace("-", "").replace("&", "")  + '.MX'
        stocks.append(symbol)
    return stocks



# página de donde se descargan los símbolos
url = 'https://en.wikipedia.org/wiki/Indice_de_Precios_y_Cotizaciones'
symbols = getSymbols(url)
# descarga de datos
currentDate = str(datetime.now())[:10]
print(currentDate)
#data = yf.download(symbols, "2012-01-03", "2022-10-01")
data = yf.download(symbols, "2012-01-03", currentDate)
data.index = pd.to_datetime(data.index)
data.head()


close = data['Close'][symbols].sort_index()
open = data['Open'][symbols].sort_index()
high = data['High'][symbols].sort_index()
low = data['Low'][symbols].sort_index()
volume = data['Volume'][symbols].sort_index()



# imputación
def impute(data, percent = 0.05):
    
    n_missing_max = len(data.index)*percent
    filt_columns = data.columns[data.isna().sum() < n_missing_max]
    close_imputed = data.loc[:, filt_columns].interpolate().dropna(axis=1)
    
    return close_imputed

# melt
def melt_prices(data, colname):
    
    close_melt = pd.melt(data.dropna(axis=1).reset_index(), id_vars=['Date'])

    #close_melt = close_melt.set_index(['Date'])
    close_melt.rename(columns={'variable':'simbolo', 
                            'value': colname}, inplace=True)
    
    return close_melt.set_index(['Date', 'simbolo'])

# imputación
close_imputed = impute(close)
open_imputed = impute(open)
high_imputed = impute(high)
low_imputed = impute(low)
volume_imputed = impute(volume)
# melting
close_melt = melt_prices(close_imputed, 'close')
open_melt = melt_prices(open_imputed, 'open')
high_melt = melt_prices(high_imputed, 'high')
low_melt = melt_prices(low_imputed, 'low')
volume_melt = melt_prices(volume_imputed, 'volume')

# concat
df = pd.concat([close_melt, open_melt, high_melt, low_melt, volume_melt], axis=1)
df = df.reset_index()


# save file
df.to_excel('base_mercado.xlsx', index=False)