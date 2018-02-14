import sqlite3
def db():
   conn = sqlite3.connect('card.db')
   print ("Opened database successfully")

   conn.execute('''CREATE TABLE COLLECTION
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            GRADE            TEXT     ,
            YEAR        CHAR(50)     NOT NULL,
            MFG        CHAR(50)     NOT NULL,
            SERIES        CHAR(50)     ,
            SPORT         CHAR(50));''')
   print ("Table created successfully")

db()


