
# Imports
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import requests


# Set variables and flags
RETRY_ATTEMPS = 5
JSON_PRINT_FLAG = False
CSV_PRINT_FLAG = False
XML_PRINT_FLAG = False
FLAGGED_PRINT_FLAG = False
FINAL_PRINT_FLAG = False
CURRENCY_PRINT_FLAG = False
JSON_PATH = './data/transactions_online.json'
CSV_PATH = './data/transactions_storeA.csv'
XML_PATH = './data/transactions_partner.xml'

# Connection to the frankfurter API
response = requests.get('https://api.frankfurter.dev/v1/latest?base=USD')

# Checks whether API connected successfully else tries to establish a connection 
# Amount of retries is established by RETRY_ATTEMPS FLAG
if response.status_code != 200:
    for _ in range(RETRY_ATTEMPS):
        response = requests.get('https://api.frankfurter.dev/v1/latest?base=USD')
        if response.status_code == 200:
            break
    # Checks if connection was successful after RETRY_ATTEMPS 
    # Displays ERROR message if unsuccessful and ends program with with error code if unsuccesful else program continues
    if response.status_code != 200:
        print("ERROR: Unable to load API")
        exit(1)
    

# Gets the information from the API in JSON format
current_prices = response.json()

# This function converts currency value to USD using the data from the frankfurter API
# and returns the converted amount
def convert_currency(amount, currency):
    if currency == 'USD':
        return amount
    else:
        return amount/current_prices['rates'].get(currency)
    
# This function determines which suspicious data flags are present in a row of data
# and returns a list contain all flags present in said row
def flag(row):
    flags = []
    if row['customer_id'] == 'C--1':
        flags.append('Invalid Customer ID')
    if pd.isna(row['transaction_id']):
        flags.append('Invalid Transaction ID')
    if  pd.isna(row['date']) or row['date'] == '_':
        flags.append('Invalid Date Value')
    elif ':' in row['date']:
        flags.append('Invalid Date Value')
    elif row['date'].count('-') != 2:
        flags.append('Invalid Date Value')
    if pd.isna(row['time']):
        flags.append('Invalid Time Value')
    elif row['time'].count(':') != 3:
        flags.append('Invalid Time Value')
    elif row['time'].count(r'\+') != 1:
        flags.append('Invalid Time Value')
    if row['amount'] <= 0:
        flags.append('Invalid Amount')
    if row['currency'] not in current_prices['rates'] and row['currency'] != current_prices['base']:
        flags.append('Invalid Currency')
    if pd.isna(row['payment_method']):
        flags.append('Invalid Payment Method')
    if pd.isna(row['source_id']):
        flags.append('Invalid Source ID')
    return flags


# This function tries to open the JSON file containing the required data 
# and returns the JSON data loading into a pandas dataframe. 
# If it failed to open the JSON file it displays an error message before exiting the program with a error code       
def open_json(FilePath):
    try:
        df = pd.read_json(FilePath)
        return df
    except:
        print("ERROR: Invalid Path for JSON file")
        return -1
    
# This function tries to open the CSV file containing the required data 
# and returns the CSV data loading into a pandas dataframe. 
# If it failed to open the CSV file it displays an error message before exiting the program with a error code     
def open_csv(FilePath):
    try:
        df = pd.read_csv(FilePath)
        return df
    except:
        print("ERROR: Invalid Path for CSV file")
        return -1

# This function tries to open the XML file containing the required data 
# and returns the XML data loading into a pandas dataframe. 
# If it failed to open the XML file it displays an error message before exiting the program with a error code     
def open_xml(FilePath):
    try:
        root = ET.parse(FilePath).getroot()
        partner_name = root.get('partner')
        rows = []
        for tx in root.findall('.//Transaction'):
            cust = tx.find('Customer')
            pay = tx.find('Payment')
            amt = tx.find('Amount')
            rows.append({
                'transaction_id': tx.get('id'),
                'customer_id': (cust.get('id') if cust is not None and cust.get('id','').strip() else 'C--1'),
                'amount': (amt.text.strip() if amt is not None and amt.text else None),
                'currency': (amt.get('currency') if amt is not None else None),
                'when_raw': tx.findtext('When'),
                'payment_method': (pay.get('method') if pay is not None else None),
                'payment_last4': (pay.get('last4') if pay is not None else None),
                'source_id': partner_name,
            })

        df = pd.DataFrame(rows)
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['when'] = pd.to_datetime(df['when_raw'], errors='coerce', utc=True)
        df = df[['transaction_id','customer_id','amount','currency','when','payment_method','payment_last4','when_raw','source_id']]
        return df
    except:
        print('ERROR: Invalid Path for XML file')
        return -1



# This section cleans and standardise the columns from the JSON file
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_json = open_json(JSON_PATH)
    df_json.rename(columns = {'id': 'transaction_id'}, inplace=True)
    df_json.rename(columns = {'channel': 'source_id'}, inplace=True)
    df_json['customer_id'] = df_json['customer'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    df_json['customer_id'] = df_json['customer_id'].fillna('C--1')
    df_json['payment_method'] = df_json['payment'].apply(lambda x: x.get('method') if isinstance(x, dict) else None)
    df_json['amount'] = df_json['total'].apply(lambda x: x.get('amount') if isinstance(x, dict) else None)
    df_json['currency'] = df_json['total'].apply(lambda x: x.get('currency') if isinstance(x, dict) else None)
    df_json[['date', 'time']] = df_json['occurred_at'].astype('string').str.replace(r'[a-zA-Z]', ' ', regex=True).str.strip().str.split(' ', expand=True)
    mask = df_json['date'].str.contains(':')
    df_json.loc[mask, ['date', 'time']] = df_json.loc[mask, ['time', 'date']].values
    df_json.drop(columns=['occurred_at'])
except:
    print("ERROR: Incorrect JSON file format")
    exit(1)

# This section cleans and standardise the columns from the CSV file
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_csv = open_csv(CSV_PATH)
    df_csv['customer_id'] = pd.to_numeric(df_csv['customer_id'], errors='coerce').fillna(-1).astype(int)
    df_csv['customer_id'] = 'C-' + df_csv['customer_id'].astype('string') 
    df_csv[['date', 'time']] = df_csv['timestamp'].astype('string').str.replace(r'[a-zA-Z]', ' ', regex=True).str.strip().str.split(' ', expand=True)
    df_csv.drop(columns=['timestamp'], inplace=True)
    df_csv.rename(columns = {'store_id': 'source_id'}, inplace=True)
    mask = df_csv['date'].str.contains(':')
    df_csv.loc[mask, ['date', 'time']] = df_csv.loc[mask, ['time', 'date']].values
    
except:
    print("ERROR: Incorrect CSV file format")
    exit(1)
df_csv.fillna(pd.NA)
# This section cleans and standardise the columns from the XML file
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_xml = open_xml(XML_PATH)
    df_xml['customer_id'] = pd.to_numeric(df_xml['customer_id'], errors='coerce').fillna(-1).astype(int)
    df_xml['customer_id'] = 'C-' + df_xml['customer_id'].astype('string') 
    df_xml[['date', 'time']] = df_xml['when_raw'].astype('string').str.replace(r'[a-zA-Z]', ' ', regex=True).str.strip().str.split(' ', expand=True)
    df_xml['time'] = df_xml['time'] + str('+00:00')
    df_xml.drop(columns=['when_raw'], inplace=True)
    df_xml.rename(columns = {'source': 'source_id'}, inplace=True)
    mask = df_xml['date'].str.contains(':')
    df_xml.loc[mask, ['date', 'time']] = df_xml.loc[mask, ['time', 'date']].values
except:
    print("ERROR: Incorrect XML file format")
    exit(1)



# This section merges the now standardised data from the various sources
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_final = pd.concat([df_json[['customer_id', 'transaction_id','date', 'time', 'amount', 'currency', 'payment_method', 'source_id']], df_csv[['customer_id', 'transaction_id','date', 'time', 'amount', 'currency', 'payment_method', 'source_id']]], ignore_index=True)
    df_final = pd.concat([df_final, df_xml[['customer_id', 'transaction_id','date', 'time', 'amount', 'currency', 'payment_method', 'source_id']]], ignore_index=True)
except:
    print("ERROR: Failed to merge dataframes")
    exit(1)

# This section collects suspicious data into a dataframe so as to be easily examined
# This section adds a flags column to the new dataframe which is generated using the flag method
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_flag = pd.concat([df_final[df_final['amount'] <= 0], df_final[df_final['customer_id'].str.contains('C--1', na=False)], df_final[pd.isna(df_final['transaction_id'])],
                         df_final[df_final['date'] == '_'], df_final[pd.isna(df_final['time'])], df_final[pd.isna(df_final['payment_method'])],
                         df_final[pd.isna(df_final['source_id'])], df_final[df_final['date'].str.contains(':', na=False)], df_final[pd.isna(df_final['date'])],
                         df_final[df_final['date'].fillna("").str.count('-') != 2], df_final[df_final['time'].fillna("").str.count(':') != 3], df_final[df_final['time'].fillna("").str.count(r'\+') != 1]], ignore_index=True)
    df_flag = df_flag.drop_duplicates()
    df_flag['flags'] = df_flag.apply(flag, axis=1)
except:
    print("ERROR: Failed to create flagged output dataframe")
    exit(1)


# This section removes suspicious from the clean dataframe
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_final = df_final[~df_final['customer_id'].str.contains('C--1', na=False)]
    df_final = df_final[~df_final['date'].str.contains(':', na=False)]
    df_final = df_final[~pd.isna(df_final['transaction_id'])]
    df_final = df_final[df_final['date'] != '_']
    df_final = df_final[~pd.isna(df_final['date'])]
    df_final = df_final[df_final['date'].fillna("").str.count('-') == 2]
    df_final = df_final[~pd.isna(df_final['time'])]
    df_final = df_final[df_final['time'].fillna("").str.count(':') == 3]
    df_final = df_final[df_final['time'].fillna("").str.count(r'\+') == 1]
    df_final = df_final[df_final['amount'] > 0]
    df_final = df_final[~pd.isna(df_final['payment_method'])]
    df_final = df_final[~pd.isna(df_final['source_id'])]
except:
    print("ERROR: Failed to remove suspecious entries")
    exit(1)


# This section converts all the amount values in the clean dataframe to USD
# The convert_currency method if used to achive this
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_final['amount'] = [convert_currency(a,c) for a,c in zip(df_final['amount'], df_final['currency'])]
    df_final['currency'] = 'USD'
    df_final.reset_index()
except:
    print("ERROR: Failed to convert values to USD")
    exit(1)



# This section uses flags set initially to determine which dataframes to display for quick analysis or debugging
# Default all print flags set to False
if JSON_PRINT_FLAG:
    print(df_json)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
if CSV_PRINT_FLAG:
    print(df_csv)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
if XML_PRINT_FLAG:
    print(df_xml)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
if FLAGGED_PRINT_FLAG:
    print(df_flag)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
if FINAL_PRINT_FLAG:
    print(df_final)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
if CURRENCY_PRINT_FLAG:
    print(current_prices)


# Final section saves clean and flagged dataframes to seperate CSV files for use by analyst
# if the section encounters an error the program displays an error message before exiting with an error code
try:
    df_flag.to_csv('./output/FlaggedEntries.csv', index=False)
    df_final.to_csv('./output/CleanEntries.csv', index=False)
except:
    print("ERROR: Failed to save clean and flagged dataframe as csv")
    exit(1)