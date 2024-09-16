import re
from database.default import cursor, db

payload ="""
{ sheetName: 'Sheet1',
  row: 7,
  column: 1,
  oldValue: 'hello',
  newValue: undefined }"""

def delete_from_db(sheet_name, column, oldValue):
    # Fetch column names from the database
    cursor.execute(f'SELECT * FROM "{sheet_name}" LIMIT 0')
    column_names = [desc[0] for desc in cursor.description]

    # Map the column number to the specific column name
    column_name = column_names[column - 1]

    # Execute the DELETE SQL query
    try:
        cursor.execute(f'DELETE FROM "{sheet_name}" WHERE "{column_name}" = %s', (oldValue,))
        db.commit()
        print(f"Deleted rows from {sheet_name} where {column_name} = {oldValue}")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

def update_in_db(table_name,column,oldValue,newValue):
    pass

def create_in_db(table_name,column,newValue):
    pass

def parse_payload(payload):
    # Regular expression to match key-value pairs
    pattern = re.compile(r"(\w+):\s*('.*?'|\d+|undefined)")
    
    # Find all matches
    matches = pattern.findall(payload)
    
    # Convert matches to a dictionary
    result = {}
    for key, value in matches:
        if value == 'undefined':
            result[key] = None
        elif value.startswith("'") and value.endswith("'"):
            result[key] = value.strip("'")
        else:
            result[key] = int(value)
    
    return result


def perform_operation_on_db(payload):
    payload = parse_payload(payload)
    sheet_name = payload.get('sheetName')
    newValue = payload.get('newValue') 
    oldValue = payload.get('oldValue')
    column = payload.get('column')

    if newValue == None:
        print("del")
        delete_from_db(sheet_name, column, oldValue)
    elif newValue != None and oldValue != None:
        print("updates")
        update_in_db(sheet_name, column, oldValue, newValue)
    else:
        print("create")
        create_in_db(sheet_name,column,newValue)
    

perform_operation_on_db(payload)