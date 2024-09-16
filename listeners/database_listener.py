import psycopg2
import asyncio
import sys
import os 
from dotenv import load_dotenv
from create_triggers import *

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
sheets_dir = os.path.join(parent_dir, 'sheets')
sys.path.insert(0, sheets_dir)
from sheets.default import *

load_dotenv()


async def listen_to_changes(table_name):
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Create function and trigger if they don't exist
    create_triggers(cur, table_name)

    # Listen for notifications
    cur.execute(f"LISTEN {table_name}_inserts;")
    cur.execute(f"LISTEN {table_name}_updates;")
    cur.execute(f"LISTEN {table_name}_deletes;")
    print(f"Listening for changes on table: {table_name}")


    while True:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            perform_operation_on_sheet(table_name, notify.payload)
        await asyncio.sleep(1)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide the table name as an argument.")
        sys.exit(1)
    table_name = sys.argv[1]
    asyncio.run(listen_to_changes(table_name))