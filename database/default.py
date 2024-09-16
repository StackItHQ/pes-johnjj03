import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
def db_setup():
    db = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user="postgres",
        password=os.getenv('DB_PASSWORD'),
        dbname=os.getenv('DB_NAME')
    )
    cursor = db.cursor()
    return db,cursor

# Function to read data from the database
def read_all_from_db(sheet_name):
    TABLE_NAME = sheet_name
    db, cursor = db_setup()

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

