import sqlite3
import os

class Database_cl(object):
    def __init__(self):
        self.dbpath = os.path.join(os.path.dirname(__file__) + 'payouts.sqlite3')
        self.connection = self.db_connect(self.dbpath)
        self.cur = self.connection.cursor()
    def db_connect(self, db_path):
        con = sqlite3.connect(db_path,check_same_thread=False)
        return con

    def createTable(self):
        links_sql = "CREATE TABLE payouts (ID text PRIMARY KEY, address text NOT NULL, ammount text NOT NULL)"
        self.cur.execute(links_sql)

    def insertEntry(self, ID, address, ammount):
        link_sql = "INSERT INTO payouts (ID, address, ammount) VALUES (?, ?, ?)"
        self.cur.execute(link_sql, (str(ID), str(address), str(ammount)))
        self.connection.commit()

    def getDB(self):
        self.cur.execute("SELECT * FROM payouts")
        return self.cur.fetchall()
        
    def deleteEntry(self, ID):
        link_sql = "DELETE FROM payouts WHERE ID = " + str(ID)
        self.cur.execute(link_sql)
        self.connection.commit()

    def deleteTimeout(self):
        link_sql = "DELETE FROM payouts WHERE datetime(timestamp) <= datetime('now','-11 minutes', 'localtime')"
        self.cur.execute(link_sql)
        self.connection.commit()

    def closeConnection(self):
        self.connection.commit()    
