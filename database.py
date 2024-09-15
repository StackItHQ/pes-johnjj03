import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()

# Database setup
db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
cursor = db.cursor()


# Function to read data from the database
def read_from_db(sheet_name):
    TABLE_NAME = sheet_name
    try:
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    except Exception as e:
        print(f"Error: {e}")
        return [], []
    
    # Fetch all rows
    result = cursor.fetchall()
    
    # Get column names
    column_names = [desc[0] for desc in cursor.description]
    
    return column_names, result

# Function to write all data from sheets to the database
def write_all_to_db(sheet_name,column_names,data):
    TABLE_NAME = sheet_name

    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")

    # Creates the query as a string to create the table with the columns
    create_table_query = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    {', '.join([f'`{col}` VARCHAR(255)' for col in column_names])}
);
""".format()

    cursor.execute(create_table_query)

    #iteratively inserts the data into the table
    for row in data[1:]:
    # Construct the query
        query = f"INSERT INTO {TABLE_NAME} ({', '.join([f'`{col}`' for col in column_names])}) VALUES ({', '.join(['%s'] * len(row))});"
        cursor.execute(query, row)

    db.commit()

# Function to update data in the database
def update_db(sheet_name,data):
    TABLE_NAME = 'your_table'
    cursor.executemany("UPDATE %s SET col1=%s, col2=%s, col3=%s, col4=%s WHERE id=%s", (TABLE_NAME,data))
    db.commit()

# Function to delete data from the database
def delete_from_db(sheet_name,ids):
    TABLE_NAME = 'your_table'
    cursor.executemany("DELETE FROM %s WHERE id=%s", (TABLE_NAME,ids))
    db.commit()