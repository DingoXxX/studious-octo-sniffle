import sqlite3

# Connect to the existing database
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f"- {table[0]}")

# For each table, get the column information
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\nColumns in table {table_name}:")
    for column in columns:
        print(f"- {column[1]} ({column[2]}) {'PRIMARY KEY' if column[5] else ''}")

cursor.close()
conn.close()
