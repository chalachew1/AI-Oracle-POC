import sqlite3

conn = sqlite3.connect("meter_connections_demo.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS meter_connections")

cur.execute("""
CREATE TABLE meter_connections (
    meter_id TEXT,
    connection_date TEXT,
    transformer_id TEXT,
    substation_id TEXT,
    status TEXT
)
""")

data = [
    ("M001", "2026-01-05", "T100", "Substation A", "active"),
    ("M002", "2026-01-10", "T100", "Substation A", "active"),
    ("M003", "2026-01-15", "T101", "Substation B", "active"),
    ("M004", "2026-02-02", "T102", "Substation B", "pending"),
    ("M005", "2026-02-10", "T100", "Substation C", "active")
]

cur.executemany("INSERT INTO meter_connections VALUES (?, ?, ?, ?, ?)", data)

conn.commit()
conn.close()

print("SQLite database created.")