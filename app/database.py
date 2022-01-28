import sqlite3
import os

class Database_cl(object):
    def __init__(self):
        self.dbpath = os.path.join(os.path.dirname(__file__) + 'database.sqlite3')
        self.connection = self.db_connect(self.dbpath)
        self.cur = self.connection.cursor()
    def db_connect(self, db_path):
        con = sqlite3.connect(db_path,check_same_thread=False)
        return con

    def createTable(self):
        links_sql = "CREATE TABLE gambles (ID text PRIMARY KEY, privateKey text NOT NULL, publicKey text NOT NULL, returnAdr text NOT NULL, chatid text NOT NULL, seed text NOT NULL, won text NOT NULL, timestamp date NOT NULL)"
        self.cur.execute(links_sql)

    def insertEntry(self, ID, privateKey, publicKey, returnAdr, chatid, seed, won, timestamp):
        link_sql = "INSERT INTO gambles (ID, privateKey, publicKey, returnAdr, chatid, seed, won, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.cur.execute(link_sql, (str(ID), str(privateKey), str(publicKey), str(returnAdr), str(chatid), str(seed), str(won), str(timestamp)))
        self.connection.commit()

    def getDB(self):
        self.cur.execute("SELECT * FROM gambles")
        return self.cur.fetchall()
        
    def deleteEntry(self, ID):
        link_sql = "DELETE FROM gambles WHERE ID = " + str(ID)
        self.cur.execute(link_sql)
        self.connection.commit()

    def deleteTimeout(self):
        link_sql = "DELETE FROM gambles WHERE datetime(timestamp) <= datetime('now','-11 minutes', 'localtime')"
        self.cur.execute(link_sql)
        self.connection.commit()

    def closeConnection(self):
        self.connection.commit()    