import os
import sys

# Add the app directory to path
sys.path.append('.')

# Remove the old database if it exists
if os.path.exists('bank.db'):
    try:
        os.remove('bank.db')
        print("Removed old bank.db")
    except Exception as e:
        print(f"Could not remove bank.db: {e}")
        exit(1)

# Use SQLAlchemy to create the database schema using our models.py 
from app.database import Base, engine
from app.models import User, Account, Transaction

# Create all tables based on Base metadata
Base.metadata.create_all(bind=engine)

# Verify the tables were created
import sqlite3
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

try:
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Successfully created new database with correct schema.")
    print("Tables created:")
    for table in tables:
        print(f"- {table[0]}")
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id)')
    
    conn.commit()
    
    # Print users table schema
    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()
    print("\nUsers table schema:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")
        
    # Print accounts table schema
    cursor.execute("PRAGMA table_info(accounts);")
    columns = cursor.fetchall()
    print("\nAccounts table schema:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")

except sqlite3.Error as e:
    conn.rollback()
    print(f"Database error: {e}")
finally:
    cursor.close()
    conn.close()
