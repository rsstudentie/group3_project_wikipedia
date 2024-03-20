import sqlite3

# Connect to the existing SQLite database
conn_existing = sqlite3.connect('wikipedia.db')
cursor_existing = conn_existing.cursor()

# Step 1: Find the top 100 pages based on total visits
query_top_pages = '''
    SELECT Page, SUM(Visits) as TotalVisits
    FROM page_visits  
    GROUP BY Page
    ORDER BY TotalVisits DESC
    LIMIT 100
'''
cursor_existing.execute(query_top_pages)
top_pages = cursor_existing.fetchall()

# Connect to the new SQLite database (this will create the file)
conn_new = sqlite3.connect('wikitop100.db')
cursor_new = conn_new.cursor()

# Step 2: Create a new table in the new database
cursor_new.execute('''
    CREATE TABLE IF NOT EXISTS page_visits (
        Page TEXT,
        Date TEXT,
        Visits INTEGER
    )
''')

# Step 3: For each top page, select all records and insert them into the new database
for page, _ in top_pages:
    cursor_existing.execute('SELECT Page, Date, Visits FROM page_visits5 WHERE Page = ?', (page,))
    page_records = cursor_existing.fetchall()
    cursor_new.executemany('INSERT INTO page_visits (Page, Date, Visits) VALUES (?, ?, ?)', page_records)

conn_new.commit()

# Close both connections
conn_existing.close()
conn_new.close()
