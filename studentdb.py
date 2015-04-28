import sqlite3

with sqlite3.connect("students.db") as connection :
    c = connection.cursor()
#    c.execute("BEGIN")
    c.execute("""CREATE TABLE student (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                mark INTEGER)""")

    c.execute('INSERT INTO student VALUES (0, "abc", "def", 90)')
    c.execute('INSERT INTO student VALUES (1, "ghi", "jkl", 91)')
    c.execute('INSERT INTO student VALUES (2, "mno", "pqr", 92)')
#    c.execute("COMMIT")
