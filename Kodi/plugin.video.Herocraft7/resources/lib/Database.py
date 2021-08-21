import sqlite3
class Database:
    def __init__(self):
        self.con = sqlite3.connect('Database.db')
        self.cur = self.con.cursor()
    def Connection(self):
        pass
    def Put_Channels(self,title,link,thumbnail):
        pass
    def Get_Channels(self):
        channels=self.cur.execute('SELECT * from channels')
        rows = channels.fetchall()
        print(rows)
        return rows
    def Submit(self):
        self.con.commit()
    def insert(self,title,link,thumbnail):
        sql="""INSERT INTO channels(title,link,thumbnail) VALUES("{0}","{1}","{2}")""".format(title,link,thumbnail)
        self.cur.execute(sql)
        self.Submit()
    def remove(self,id):
        sql_delete_query = """DELETE from channels where ID={0}""".format(id)
        self.cur.execute(sql_delete_query)
        self.Submit()
        
    def CreateTable(self):
        self.cur.execute('''CREATE TABLE channels(id integer PRIMARY KEY,title,link,thumbnail)''')
        self.Submit()
    def Connection_Close(self):
        self.con.close()
database=Database()
#database.CreateTable()
#database.Get_Channels()
#database.insert("jack2","jack3","jack4")
database.Get_Channels()



database.Connection_Close()