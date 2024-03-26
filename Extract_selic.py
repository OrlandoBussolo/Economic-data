import yfinance as yf
import pandas as pd
import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import mysql.connector
import os

def data_selic_extract():

    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4189/dados?formato=json"
    response = requests.get(url)
    data_selic = pd.DataFrame(response.json())

    # Renomear colunas
    data_selic.rename(columns={'data': 'Date', 'valor': 'Value'}, inplace=True)

    # Converter a coluna 'Date' para o formato correto (dia/mês/ano)
    data_selic['Date'] = pd.to_datetime(data_selic['Date'], format='%d/%m/%Y')
    return data_selic


def create_date_table():
    start_date = datetime.strptime('2000-01-01', '%Y-%m-%d')
    dates = []
    end_date = datetime.today()
    current_date = start_date
    while current_date <= end_date:
        dates.append((current_date,))
        current_date += timedelta(days=1)
    date_table = pd.DataFrame(dates, columns=['Date'] ) 
    date_table = date_table.reset_index(drop=True)  
    return date_table

def merge(df1,df2):
    result = pd.merge(df1, df2, on='Date', how='left')
    return result

def selic_data_correct(dataframe):
    a = []
    last_valid_value = np.nan  # Inicialmente, nenhum valor válido foi encontrado
    # Iterar sobre os valores do DataFrame 'result'
    for i in range(len(dataframe)):
        # Verificar se o valor na coluna 'value' é NaN para a linha atual
        if pd.notna(dataframe.at[i, 'Value']):
            last_valid_value = dataframe.at[i, 'Value']
            a.append(dataframe.at[i, 'Value'])       
        else:
            a.append(last_valid_value)

    if 'Value_daily' in dataframe.columns:
        print("A coluna 'Value_daily' já existe no DataFrame.")
        # Coloque aqui o código que você deseja executar se a coluna já existir
    else:
        # Se a coluna 'Value_daily' não existir, crie uma nova série e adicione-a ao DataFrame
        serie = pd.Series(a, name='Value_daily')
        df_corrected = pd.concat([dataframe, serie], axis=1) 
    return df_corrected  
#------------------------------------------------------------------------------------------------------------

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
        Date         DATE, 
        Selic        FLOAT, 
        Selic_Daily  FLOAT, 

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
    sql = f"INSERT INTO {db_name}.{tb_name} VALUES (%s,%s,%s)"

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
    create_table(cursor, "db_stocks", "selic_rate")
    show_tables(cursor, "db_stocks")

    # reading and adding data
    selic_data = data_selic_extract()
    date_table = create_date_table()
    merge_data = merge(date_table, selic_data)
   
    correct_data = selic_data_correct(merge_data)

    add_data(cnx, cursor, correct_data, "db_stocks", "selic_rate")
    cnx.close()



        
