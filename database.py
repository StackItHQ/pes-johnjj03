import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
db = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user="postgres",
    password=os.getenv('DB_PASSWORD'),
    dbname=os.getenv('DB_NAME')
)
cursor = db.cursor()

# Function to read data from the database
def read_all_from_db(sheet_name):
    TABLE_NAME = sheet_name
    try:
        cursor.execute(f'SELECT * FROM "{TABLE_NAME}"')
    except Exception as e:
        print(f"Error: {e}")
        return [], []
    
    # Fetch all rows
    result = cursor.fetchall()
    
    # Get column names
    column_names = [desc[0] for desc in cursor.description]
    
    return column_names, result

# Function to write all data from sheets to the database
def write_all_to_db(sheet_name, column_names, data):
    table_name = sheet_name

    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')

    # Creates the query as a string to create the table with the columns
    create_table_query = f"""
CREATE TABLE IF NOT EXISTS "{table_name}" (
    {', '.join([f'"{col}" VARCHAR(255)' for col in column_names])}
);
"""

    cursor.execute(create_table_query)

    query = f"""
    INSERT INTO {table_name} ({', '.join([f'"{col}"' for col in column_names])}) 
    VALUES ({', '.join(['%s'] * len(column_names))})
    """
    for row in data[1:]:
        cursor.execute(query, row)
        pass

    db.commit()
