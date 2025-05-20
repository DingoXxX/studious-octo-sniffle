import sqlite3

conn = sqlite3.connect('bank.db')
c = conn.cursor()

try:
    c.execute('ALTER TABLE accounts ADD COLUMN is_bank_linked INTEGER NOT NULL DEFAULT 0;')
    print('Added is_bank_linked to accounts')
except Exception as e:
    print('is_bank_linked:', e)

try:
    c.execute('ALTER TABLE accounts ADD COLUMN is_bank_verified INTEGER NOT NULL DEFAULT 0;')
    print('Added is_bank_verified to accounts')
except Exception as e:
    print('is_bank_verified:', e)

try:
    c.execute('ALTER TABLE transactions ADD COLUMN transfer_type TEXT;')
    print('Added transfer_type to transactions')
except Exception as e:
    print('transfer_type:', e)

try:
    c.execute("ALTER TABLE transactions ADD COLUMN status TEXT NOT NULL DEFAULT 'pending';")
    print('Added status to transactions')
except Exception as e:
    print('status:', e)

conn.commit()
conn.close()
print('Migration complete.')
