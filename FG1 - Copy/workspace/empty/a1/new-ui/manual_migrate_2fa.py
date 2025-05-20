import sqlite3

conn = sqlite3.connect('bank.db')
c = conn.cursor()

try:
    c.execute('ALTER TABLE users ADD COLUMN twofa_secret TEXT;')
    print('Added twofa_secret to users')
except Exception as e:
    print('twofa_secret:', e)

try:
    c.execute('ALTER TABLE users ADD COLUMN twofa_enabled INTEGER NOT NULL DEFAULT 0;')
    print('Added twofa_enabled to users')
except Exception as e:
    print('twofa_enabled:', e)

conn.commit()
conn.close()
print('2FA migration complete.')
