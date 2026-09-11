import sqlite3
import csv

# Connect to SQLite using a context manager
def create_table(name):
    with sqlite3.connect(f"./db_files/{name}.db") as connection:
        cursor = connection.cursor()

        # Create employees table if not exists
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase_id INTEGER NOT NULL,
                sentence_id INTEGER NOT NULL,
                phrase TEXT NOT NULL,
                type TEXT NOT NULL,
                bundle_id INTEGER NOT NULL,
                preceeded_by INTEGER NOT NULL,
                leads_to INTEGER NOT NULL,
                xmin INTEGER NOT NULL,
                ymin INTEGER NOT NULL,
                xmax INTEGER NOT NULL,
                ymax INTEGER NOT NULL,
                Page INTEGER NOT NULL,
                Total_Sentences INTEGER NOT NULL
            )
        ''')
def get_word_count(name):
    with sqlite3.connect(f"./db_files/{name}.db") as connection:
        cursor = connection.cursor()

        # Create employees table if not exists
        cursor.execute(f'''
            SELECT DISTINCT COUNT(phrase) AS word_count FROM {name}
        ''')
        #print(cursor.fetchall())
        return cursor.fetchall()[0][0]
    #print("Database and table setup complete.")
#phrase_id,sentence_id,phrase,type,bundle_id,preceeded_by,leads_to,xmin,ymin,xmax,ymax,Page,Total_Sentences

def import_contents(name):
    # Connect to database using context manager
    with sqlite3.connect(f"./db_files/{name}.db") as connection:
        cursor = connection.cursor()
        
        # Open CSV file using context manager and insert data
        with open(f"data/dict/working_set/traversable_text/{name}_traversable.csv", mode="r") as file:
            reader = csv.reader(file)
            reader.__next__()  # Skip the header row
            data = list(reader)  # Read all remaining rows
        
        # Execute bulk insert
        cursor.executemany(f"INSERT INTO {name} (phrase_id,sentence_id,phrase,type,bundle_id,preceeded_by,leads_to,xmin,ymin,xmax,ymax,Page,Total_Sentences) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    #print("CSV data successfully inserted into SQLite.")

def traverse_db(name):
    # Using context manager to fetch data
    with sqlite3.connect(f"./db_files/{name}.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {name}")
        # Iterate over the cursor for efficient memory use
        for row in cursor:
            print(row)

def search(name,sentence_id,bundle_id):
    rows = []
    with sqlite3.connect(f"./db_files/{name}.db") as connection:
        cursor = connection.cursor()
        #print(f"Name (sqlite): {name}")
        #print(f"id (sqlite): {sentence_id}")
        cursor.execute(f"SELECT * FROM {name} WHERE sentence_id = {sentence_id} AND phrase IS NOT '[]'")
        for row in cursor:
            #print(f"cursor row: {row}")
            rows.append(row)
    return rows

def initialize(name):
    create_table(name)
    import_contents(name)