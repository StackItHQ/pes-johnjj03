import os 
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv


from utils import read_all_from_sheet

load_dotenv()

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

def update_operation_on_sheet(sheet_name, data):
    # Initialize the Google Sheets API service
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Extract column names, old values, and new values from data
    column_names, old_values, new_values = data

    # Read all data from the sheet
    all_column_names, values = read_all_from_sheet(sheet_name)
    if not values:
        print("Sheet does not exist or is empty.")
        return

    # Find the indices of the columns to update
    column_indices = [all_column_names.index(col) for col in column_names]

    # Find the rows to update
    rows_to_update = []
    for i, row in enumerate(values[1:], start=1):  # Skip the header row
        if not row: #skip empty rows
            continue
        if all(row[idx] == val for idx, val in zip(column_indices, old_values)):
            rows_to_update.append(i)

    # Update the rows
    for row_index in rows_to_update:
        range_name = f'{sheet_name}!A{row_index + 1}:Z{row_index + 1}'
        row_data = values[row_index]
        for idx, new_val in zip(column_indices, new_values):
            row_data[idx] = new_val
        body = {'values': [row_data]}
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

    print(f"Updated {len(rows_to_update)} rows in {sheet_name}.")