import os 
import sys
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
sheets_dir = os.path.join(parent_dir, 'sheets')
sys.path.insert(0, sheets_dir)

from api import sheets_api_setup
from utils import *

load_dotenv()

# Google Sheets API setup
SCOPES = [].append(os.getenv('SCOPES'))
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
sheet = sheets_api_setup()

def delete_operation_on_sheet(sheet_name, data):

    # Read all data from the sheet
    column_names, values = read_all_from_sheet(sheet_name)
    if not values:
        print("Sheet does not exist or is empty.")
        return

    # Prepare the data to be deleted
    columns_to_delete = data[0]
    values_to_delete = data[1]

    # Find the indices of the columns to delete
    column_indices = [column_names.index(col) for col in columns_to_delete]

    # Find the rows to delete
    rows_to_delete = []
    for i, row in enumerate(values[1:], start=1):  # Skip the header row
        if not row: # Skip empty rows
            continue
        if all(row[idx] == val for idx, val in zip(column_indices, values_to_delete)):
            rows_to_delete.append(i)

    # Delete the rows in reverse order to avoid index shifting
    for row_index in reversed(rows_to_delete):
        range_name = f'{sheet_name}!A{row_index + 1}:Z{row_index + 1}'
        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()

    print(f"Deleted {len(rows_to_delete)} rows from {sheet_name}.")