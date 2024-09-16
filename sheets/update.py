import os 
from dotenv import load_dotenv
from api import sheets_api_setup
from utils import read_all_from_sheet

load_dotenv()

# Google Sheets API setup
sheet = sheets_api_setup()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SCOPES = [].append(os.getenv('SCOPES'))

def update_operation_on_sheet(sheet_name, data):
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