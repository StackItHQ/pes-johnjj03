import json
from database.default import *
from database.insert import *
from sheets.default import *
from sheets.insert import *
import subprocess

def write_sheets_to_db(sheet_name):
    column_names, data = read_all_from_sheet(sheet_name)
    if not data:
        print("Sheet does not exist in the document.")
        return
    table_name = sheet_name
    write_all_to_db(table_name,column_names,data)
    return table_name

def write_db_to_sheets(table_name):
    column_names, data = read_all_from_db(table_name)
    if not data:
        print("Table does not exist in the database.")
        return
    sheet_name = table_name
    write_all_to_sheet(sheet_name,column_names,data)
    return sheet_name



def main():
    
    # Initialize the configuration dictionary
    config = {
        "google_sheets_priority": 0,
        "post_database_priority": 0
    }

    if os.path.exists('priority.json'):
        with open('priority.json', 'r') as config_file:
            config = json.load(config_file)
    
    else:
        while True:
            # Set the priority based on the user's choice
            choice = input("Do you prefer to start with Google Sheets or PostgreSQL? (Enter 'google' or 'post'): ").strip().lower()
            if choice == 'google':
                config["google_sheets_priority"] = 1
                break
            elif choice == 'post':
                config["post_database_priority"] = 1
                break
            else:
                print("Invalid choice. Please enter 'google' or 'post'.")

        with open('priority.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    

    if config["google_sheets_priority"] == 1:
        sheet_name = input("Enter the name of the Sheet you want to sync with the database: ")
        table_name = write_sheets_to_db(sheet_name)
    
    elif config["post_database_priority"] == 1:
        table_name = input("Enter the name of the table you want to sync with Google Sheets: ")
        sheet_name = write_db_to_sheets(table_name)

    print("Sync completed.")

    subprocess.run(["python", "./listeners/db_listener.py",table_name],shell=True,text=True)

    pass

if __name__ == "__main__":
    main()