import sqlite3

class OADB:

    def __init__(self):
        self.conn = sqlite3.connect("db/oadb.db")
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS links (ID INTEGER PRIMARY KEY AUTOINCREMENT, Link TEXT UNIQUE, Alive INTEGER DEFAULT 1, LastScraped INTEGER, Site INTEGER)')
        self.c.execute('CREATE TABLE IF NOT EXISTS items (ID INTEGER PRIMARY KEY AUTOINCREMENT, LID INTEGER, Link TEXT, AID INTEGER DEFAULT 0, Discont INTEGER DEFAULT 0,Name Text, Price REAL, Amount INTEGER, Volume INTEGER, Format Text, Alcohol REAL, Type TEXT, Cat1 TEXT, Cat2 TEXT, CONSTRAINT fkey FOREIGN KEY(LID) REFERENCES links(ID) ON DELETE CASCADE)')
        self.conn.commit()

    def startBeerLinks(self):
        self.c.execute('UPDATE links SET Alive = 0 WHERE Site = 1')
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

    def getBeerLinks(self):
        self.c.execute('SELECT Link FROM links WHERE Site = 1 AND Alive = 1')
        r = self.c.fetchall()
        return [i[0] for i in r]

    def getBeerID(self, link):
        t = (link.encode('utf-8'),)
        self.c.execute('SELECT ID FROM links WHERE Link = ?', t)
        return self.c.fetchall()[0][0]

    def setVisited(self, i):
        t = (i,)
        self.c.execute('UPDATE links SET LastScraped = CURRENT_TIMESTAMP WHERE ID = ?', t)
        self.conn.commit()

    def endBeerLinks(self):
        self.c.execute('DELETE FROM links WHERE Alive = 0 AND Site = 1')
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
        return None
