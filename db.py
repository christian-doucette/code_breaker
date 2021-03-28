import sqlite3




def create_db_schema():
        conn = sqlite3.connect('frequencies_database.db')

        print("Creating database in frequencies_database.db, with script in create_db.sql")
        with open("create_db.sql", "r") as f:
            conn.executescript(f.read())
        print("Database schema created successfully!")


def test_db():
        conn = sqlite3.connect('frequencies_database.db')
        cur  = conn.cursor()
        #18, 19, 20, 3, 4
        #26, 26, 0, 13, 3
        #cur.execute("SELECT * FROM frequencies WHERE letter1 = 18 AND letter2 = 19 AND letter3 = 20 AND letter4 = 3 AND letter5 = 4")
        cur.execute("SELECT * FROM frequencies ORDER BY frequency DESC LIMIT 1000")

        rows = cur.fetchall()

        for row in rows:
            print(row)

        conn.close()

#create_db_schema()
test_db()
