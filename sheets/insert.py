import os 
import sys
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
sheets_dir = os.path.join(parent_dir, 'sheets')
sys.path.insert(0, sheets_dir)

from api import sheets_api_setup

load_dotenv()

# Google Sheets API setup
SCOPES = [].append(os.getenv('SCOPES'))
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')



# Function to write all data to Google Sheets
def write_all_to_sheet(sheet_name, column_names, data):
    sheet = sheets_api_setup()

    values = [column_names] + data
    body = {
        'values': values
    }

    # Define the range to update
    range_name = f'Sheet1!A1'

    # Write data to the sheet
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()



def insert_operation_on_sheet(sheet_name, data):
    sheet = sheets_api_setup()
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

