import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
db_dir = os.path.join(parent_dir, 'database')
sys.path.insert(0, db_dir)
from database.default import *

def write_all_to_db(sheet_name, column_names, data):
    db = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user="postgres",
        password=os.getenv('DB_PASSWORD'),
        dbname=os.getenv('DB_NAME')
    )
    cursor = db.cursor()

    table_name = sheet_name

    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')

    # Creates the query as a string to create the table with the columns
    create_table_query = f"""
CREATE TABLE IF NOT EXISTS "{table_name}" (
    {', '.join([f'"{col}" VARCHAR(255)' for col in column_names if col])}
);
"""

    cursor.execute(create_table_query)

    query = f"""
    INSERT INTO {table_name} ({', '.join([f'"{col}"' for col in column_names])}) 
    VALUES ({', '.join(['%s'] * len(column_names))})
    """
    
    for row in data[1:]:
        if not row:
            continue
        cursor.execute(query, row)
        pass

    db.commit()