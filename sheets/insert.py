import os 
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
sheets_dir = os.path.join(parent_dir, 'sheets')
sys.path.insert(0, sheets_dir)
from default import *

load_dotenv()

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# Function to write all data to Google Sheets
def write_all_to_sheet(sheet_name, column_names, data):
    # Initialize the Google Sheets API service
    creds = credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Prepare the data to be written
    values = [column_names] + data
    body = {
        'values': values
    }

    # Define the range to update
    range_name = f'{sheet_name}!A1'

    # Write data to the sheet
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

def insert_operation_on_sheet(sheet_name, data):
    # Initialize the Google Sheets API service
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Prepare the data to be appended
    columns = data[0]
    values = data[1:]

    # Append columns if the sheet is empty
    range_name = f'{sheet_name}!A1:Z1'
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    if not result.get('values'):
        body = {'values': [columns]}
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

    # Append data to the sheet
    range_name = f'{sheet_name}!A:Z'

    body = {'values': values}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    print(f"Inserted {len(values)} rows into {sheet_name}.")

