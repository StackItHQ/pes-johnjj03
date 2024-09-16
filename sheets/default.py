import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
sheets_dir = os.path.join(parent_dir, 'sheets')
sys.path.insert(0, sheets_dir)

from insert import *
from update import *
from delete import *
from utils import *


def perform_operation_on_sheet(sheet_name, payload):
    print(payload)
    operation = payload.split(":")[0]

    if operation == "INSERT":
        data = payload.split(":")[1]
        data = clean_data_insert_delete(payload,operation)
        insert_operation_on_sheet(sheet_name,data)
    
    elif operation == "UPDATE":
        data = clean_data_update(payload)
        update_operation_on_sheet(sheet_name,data)
    
    elif operation == "DELETE":
        data = payload.split(":")[1]
        data = clean_data_insert_delete(payload,operation)
        delete_operation_on_sheet(sheet_name,data)
    else:
        print("Invalid operation")
        return
