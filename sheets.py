import os 
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = 'Sheet1!A1:D'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# Function to read data from Google Sheets
def read_all_from_sheet(sheet_name):
    RANGE_NAME = f'{sheet_name}!A1:Z'
    try:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    except:
        print("Sheet does not exist.")
        return [], []
    values = result.get('values', [])
    column_names = values[0]
    return column_names,values

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

