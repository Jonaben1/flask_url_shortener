import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as sql:
    connection.executescript(sql.read())

connection.commit()
connection.close()
