import sqlite3

# Connect to the database
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

try:
    # Add routing_number column to accounts table
    cursor.execute("ALTER TABLE accounts ADD COLUMN routing_number TEXT;")
    
    # Add account_number column to accounts table
    cursor.execute("ALTER TABLE accounts ADD COLUMN account_number TEXT;")
    
    # Create an index on routing_number
    cursor.execute("CREATE INDEX idx_accounts_routing_number ON accounts(routing_number);")
    
    # Create a unique index on account_number
    cursor.execute("CREATE UNIQUE INDEX idx_accounts_account_number ON accounts(account_number);")
    
    conn.commit()
    print("Successfully added columns to the accounts table.")
    
    # Verify the changes
    cursor.execute("PRAGMA table_info(accounts);")
    columns = cursor.fetchall()
    print("Updated accounts schema:")
    print([col[1] for col in columns])
    
except sqlite3.Error as e:
    conn.rollback()
    print(f"Database error: {e}")
finally:
    cursor.close()
    conn.close()
