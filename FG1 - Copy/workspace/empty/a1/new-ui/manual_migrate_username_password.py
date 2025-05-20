import sqlite3

conn = sqlite3.connect('bank.db')
c = conn.cursor()

# Add username column if it doesn't exist
try:
    c.execute("ALTER TABLE users ADD COLUMN username VARCHAR")
    print("Added username column to users table.")
except sqlite3.OperationalError as e:
    print("username column may already exist:", e)

# Add hashed_password column if it doesn't exist
try:
    c.execute("ALTER TABLE users ADD COLUMN hashed_password VARCHAR")
    print("Added hashed_password column to users table.")
except sqlite3.OperationalError as e:
    print("hashed_password column may already exist:", e)

conn.commit()
conn.close()
print("Migration complete.")
