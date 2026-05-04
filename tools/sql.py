import sqlite3

db = "db.sqlite3"

print("Connected to:", db)
con = sqlite3.connect(db)
cur = con.cursor()

while True:
    query = input("sqlite> ")
    if query.lower() in ["exit", "quit", "q"]:
        break
    try:
        cur.execute(query)
        result = cur.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print("Error:", e)

con.close()
