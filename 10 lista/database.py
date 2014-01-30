import sqlite3
import sys

class Database:
    con = ""

    def connect(self, ):
        try:
            self.con = sqlite3.connect('db/db.sqlite')            

        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def disconnect(self):
        self.con.close()

    def prepare_database(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, content TEXT, type INT, start_date datetime default CURRENT_TIMESTAMP, end_date datetime default CURRENT_TIMESTAMP)')