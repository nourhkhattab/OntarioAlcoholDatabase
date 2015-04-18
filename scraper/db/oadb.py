import sqlite3
import json

class OADB:

    def __init__(self):
        self.conn = sqlite3.connect("db/oadb.db")
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS links (ID INTEGER PRIMARY KEY AUTOINCREMENT, Link TEXT UNIQUE, Alive INTEGER DEFAULT 1, LastScraped INTEGER, Site INTEGER)')
        self.c.execute('CREATE TABLE IF NOT EXISTS items (ID INTEGER PRIMARY KEY AUTOINCREMENT, LID INTEGER, Link TEXT, AID INTEGER DEFAULT 1, Discont INTEGER DEFAULT 0,Name Text, Price REAL, Amount INTEGER, Volume INTEGER, Format Text, Alcohol REAL, Type TEXT, Cat1 TEXT, Cat2 TEXT, CONSTRAINT fkey FOREIGN KEY(LID) REFERENCES links(ID) ON DELETE CASCADE)')
        self.conn.commit()

    def startBeerLinks(self):
        self.c.execute('UPDATE links SET Alive = 0 WHERE Site = 1')
        self.conn.commit()

    def startLCBOLinks(self):
        self.c.execute('UPDATE links SET Alive = 0 WHERE Site = 0')
        self.conn.commit()

    def addBeerLink(self, link):
        t = (link,)
        self.c.execute('SELECT ID FROM links WHERE Link = ?', t)
        r = self.c.fetchall()
        if len(r) == 0:
            self.c.execute('INSERT INTO links (Link, LastScraped, Site) VALUES (?,0, 1)', t)
        else:
            t = (r[0][0],)
            self.c.execute('UPDATE links SET Alive = 1 WHERE ID = ?', t)
        self.conn.commit()

    def addLCBOLink(self, link):
        t = (link,)
        self.c.execute('SELECT ID FROM links WHERE Link = ?', t)
        r = self.c.fetchall()
        if len(r) == 0:
            self.c.execute('INSERT INTO links (Link, LastScraped, Site) VALUES (?,0,0)', t)
        else:
            t = (r[0][0],)
            self.c.execute('UPDATE links SET Alive = 1 WHERE ID = ?', t)
        self.conn.commit()

    def addBeerItem(self, lID, Link, Name, Price, Amount, Volume, Format, Alcohol, Cat1, Cat2):
        t = (lID, Link)
        self.c.execute('SELECT ID FROM items WHERE LID = ? AND Link = ?', t)
        r = self.c.fetchall()
        if len(r) == 0:
            t = (lID, Link, Name, Price, Amount, Volume, Format, Alcohol, "Beer", Cat1, Cat2)
            self.c.execute('INSERT INTO items (LID, Link, AID, Name, Price, Amount, Volume, Format, Alcohol, Type, Cat1, Cat2) VALUES (?,?,1,?,?,?,?,?,?,?,?,?)', t)
        else:
            t = (Price, r[0][0])
            self.c.execute('UPDATE items SET AID = 1, Price = ? WHERE ID = ?', t)
        self.conn.commit()

    def addLCBOItem(self, lID, Link, Name, Price, Amount, Volume, Format, Alcohol, Type, Cat1, Cat2):
        t = (lID, Link)
        self.c.execute('SELECT ID FROM items WHERE LID = ? AND Link = ?', t)
        r = self.c.fetchall()
        if len(r) == 0:
            t = (lID, Link, Name, Price, Amount, Volume, Format, Alcohol, Type, Cat1, Cat2)
            self.c.execute('INSERT INTO items (LID, Link, AID, Name, Price, Amount, Volume, Format, Alcohol, Type, Cat1, Cat2) VALUES (?,?,1,?,?,?,?,?,?,?,?,?)', t)
        else:
            t = (Price, r[0][0])
            self.c.execute('UPDATE items SET AID = 1, Price = ? WHERE ID = ?', t)
        self.conn.commit()

    def getBeerLinks(self):
        self.c.execute('SELECT Link FROM links WHERE Site = 1 AND Alive = 1 AND LastScraped <= date(\'now\', \'-7 days\')')
        r = self.c.fetchall()
        return [i[0] for i in r]

    def getLCBOLinks(self):
        self.c.execute('SELECT Link FROM links WHERE Site = 0 AND Alive = 1 AND LastScraped <= date(\'now\', \'-7 days\')')
        r = self.c.fetchall()
        return [i[0] for i in r]

    def getID(self, link):
        t = (link.encode('UTF-8', 'replace'),)
        self.c.execute('SELECT ID FROM links WHERE Link = ?', t)
        r = self.c.fetchall()[0][0]
        t = (r,)
        self.c.execute('UPDATE items SET AID = 0 WHERE LID = ?', t)
        self.conn.commit()
        return r

    def setVisited(self, i):
        t = (i,)
        self.c.execute('UPDATE links SET LastScraped = CURRENT_TIMESTAMP WHERE ID = ?', t)
        self.conn.commit()

    def getItems(self):
        self.c.execute("SELECT * from items")
        r = self.c.fetchall()
        rows = [dict(rec) for rec in r]
        return json.dumps(rows)

    def endBeerLinks(self):
        self.c.execute('DELETE FROM links WHERE Alive = 0 AND Site = 1')
        self.conn.commit()

    def endLCBOLinks(self):
        self.c.execute('DELETE FROM links WHERE Alive = 0 AND Site = 0')
        self.conn.commit()

    def endItems(self):
        self.c.execute('DELETE FROM items WHERE AID = 0')
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
        return None
