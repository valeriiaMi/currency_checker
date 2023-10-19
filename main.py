import requests
import gspread
from google.oauth2 import service_account

update_from = input("Enter the update_from date (yyyy-mm-dd): ")
update_to = input("Enter the update_to date (yyyy-mm-dd): ")

# Use conditional assignment to provide default values
update_from = update_from.replace('-', '') if update_from else "20230208"
update_to = update_to.replace('-', '') if update_to else "20230208"

credentials_file = 'credentials.json'

# API endpoint for exchange rate data
api_url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={update_from}&json"

credentials = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.service_account(filename=credentials_file)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1b0dM_iRY6_aGSbBMrgrp3q69EtIH8yUMqfWneU8oW1A/edit?usp=sharing'
sh = gc.open_by_url(spreadsheet_url)
worksheet = sh.worksheet('Sheet1')

response = requests.get(api_url)
exchange_data = response.json()

response = requests.get(api_url)
exchange_data = response.json()

usd_rate = None

for row in exchange_data:
    if row['cc'] == "USD":
        usd_rate = row['rate']
        break
if usd_rate is not None:
    worksheet.update('A1', [[usd_rate]])
else:
    print("USD exchange rate data not found in the API response.")
