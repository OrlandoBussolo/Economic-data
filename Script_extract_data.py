import yfinance as yf
import pandas as pd
import requests

def get_historical_price_data(symbols):
    data_price = pd.DataFrame()  # Create an empty DataFrame to store all data
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period="max")
        data = data[['Close']]
        data.columns = [f'{symbol}_Close',]  # Add prefix to columns to differentiate symbols
        data_price = pd.concat([data_price, data], axis=1)  # Concatenate data for each symbol
    return data_price



def get_historical_volume_data(symbols):
    data_volume = pd.DataFrame()  # Create an empty DataFrame to store all data
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period="max")
        data = data[['Volume']]
        data.columns = [f'{symbol}_Volume']  # Add prefix to columns to differentiate symbols
        data_volume = pd.concat([data_volume, data], axis=1)  # Concatenate data for each symbol
    return data_volume  


def get_selic_rate():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4189/dados?formato=json"
    response = requests.get(url)
    data = pd.DataFrame(response.json())
    return data

