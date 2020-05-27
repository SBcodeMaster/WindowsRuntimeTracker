import sqlite3

class Database:
    """this class will help to add and query data"""

    def __init__(self):

        try:
            self.db = sqlite3.connect(r"E:\runtime.db")
        except :
            print("error")

        self.db.execute(
            "CREATE TABLE IF NOT EXISTS runtimeTable (sn INTEGER PRIMARY KEY AUTOINCREMENT,Datetime TEXT NOT NULL, time INTEGER, status TEXT)")
        self.cur = self.db.cursor()

    def setData(self,datestamp,status,min):

        self.cur.execute("INSERT INTO runtimeTable (Datetime, time,Status) VALUES(?,?,?)", (datestamp,min,status))
        self.cur.connection.commit()

    def __del__(self):
        self.cur.close()
        self.db.close()
