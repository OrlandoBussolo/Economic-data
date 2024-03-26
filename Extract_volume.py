import yfinance as yf
import pandas as pd
import requests

import mysql.connector
import pandas as pd
import numpy as np
import os

def get_historical_price_data(symbols):
    data_volume = pd.DataFrame()  # Create an empty DataFrame to store all data
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period="max")
        data = data[['Volume']]
        data.columns = [f'{symbol}_R$',]  # Add prefix to columns to differentiate symbols
        data_volume = pd.concat([data_volume, data], axis=1)  # Concatenate data for each symbol
    data_volume.reset_index(drop=False, inplace=True)
    df = data_volume    
    return df

def connect_mysql(host_name, user_name, pw):
    cnx = mysql.connector.connect(
        host = host_name,
        user = user_name,
        password = pw
    )
    print(cnx)
    return cnx

def create_cursor(cnx):
    cursor = cnx.cursor()
    return cursor

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"\nData Base {db_name} created")

def show_databases(cursor):
    cursor.execute("SHOW DATABASES")
    print("The databases that exists are:")
    for x in cursor:
        print(x)

def create_table(cursor, db_name, tb_name):    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {db_name}.{tb_name}(
        Date        DATE, 
        ITUB3_Vol  FLOAT, 
        BBDC4_Vol  FLOAT, 
        ROXO34_Vol FLOAT, 
        BBAS3_Vol  FLOAT, 
        SANB11_Vol FLOAT, 
        INBR32_Vol FLOAT, 
        BPAC11_Vol FLOAT,        
        PRIMARY KEY (Date)
    )""")
                   
    print(f"\nTable {tb_name} created")


def show_tables(cursor, db_name):
    cursor.execute(f"USE {db_name}")          # Set the current database
    cursor.fetchall()                         # Consuming any pending results
    cursor.execute("SHOW TABLES")              # Retrieve list of tables
    tables = cursor.fetchall()                 # Fetch all tables
    if tables:                                 # If tables exist
        for x in tables:                      # Iterate over the list of tables
            print(x)                           # Print each table name
    else:
        print("There is no table in this database")


def add_data(cnx, cursor, df, db_name, tb_name):
    lista = [tuple(row) for i, row in df.iterrows()]
    lista = [tuple(None if pd.isna(item) else item for item in tupla) for tupla in lista]
    sql = f"INSERT INTO {db_name}.{tb_name} VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.executemany(sql, lista)
    print(f"\n {cursor.rowcount} lines were inserted into table {tb_name}.")
    cnx.commit()

    # Fechar o cursor e a conexão
    cursor.close()


if __name__ == "__main__":
    
    # connecting to mysql
    pw_mysql = os.environ.get("pw_mysql")    
    cnx = connect_mysql("localhost", "orlando_bussolo", pw_mysql)
    cursor = create_cursor(cnx)

    # creating database
    create_database(cursor, "db_stocks")
    show_databases(cursor)

    # creating table
    create_table(cursor, "db_stocks", "close_volume")
    show_tables(cursor, "db_stocks")

    # reading and adding data
    df = get_historical_price_data(['ITUB3.SA','BBDC4.SA' , 'ROXO34.SA', 'BBAS3.SA', 'SANB11.SA', 'INBR32.SA', 'BPAC11.SA'])
    add_data(cnx, cursor, df, "db_stocks", "close_volume")
    cnx.close()
