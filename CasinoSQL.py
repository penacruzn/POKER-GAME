import sqlite3
database = sqlite3.connect("CasinoDB.db")

cursor = database.cursor()

# SQL command to create a table in the database 
sql_command = """CREATE TABLE GAMES (  
GAMEID TEXT PRIMARY KEY NOT NULL,
NETGAIN INTEGER NOT NULL,
GAMESALLOWED INTEGER NOT NULL,
MAXBET INTEGER NOT NULL,
TIMESPLAYED INTEGER NOT NULL)
;"""
  
# execute the statement 
#cursor.execute(sql_command) 

sql_command = """CREATE TABLE USER (  
USERID TEXT PRIMARY KEY NOT NULL,
PASSWORD TEXT NOT NULL,
NETGAIN INTEGER NOT NULL,
BALANCE INTEGER NOT NULL,
HASCHEATED TEXT NOT NULL)
;"""
  
#cursor.execute(sql_command) 

sql_command = """CREATE TABLE ADMIN (  
USERID TEXT PRIMARY KEY NOT NULL,
PASSWORD TEXT NOT NULL)
;"""

#cursor.execute(sql_command)

sql_command = """CREATE TABLE HISTORY (  
TIMESTAMP DATE PRIMARY KEY NOT NULL,
GAMEID TEXT NOT NULL,
USERID, TEXT NOT NULL,
RESULT TEXT NOT NULL,
AMOUNT INTEGER NOT NULL)
;"""
  
#cursor.execute(sql_command) 





sql_command = """INSERT INTO GAMES VALUES('Craps', 0, 5, 500, 0);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO GAMES VALUES('Black Jack', 0, 5, 2000, 0);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO GAMES VALUES('Poker', 0, 5, 1500, 0);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO GAMES VALUES('Slots', 0, 5, 250, 0);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO GAMES VALUES('Roulette', 0, 5, 2500, 0);"""
#cursor.execute(sql_command)

sql_command = """SELECT * FROM GAMES"""
cursor.execute(sql_command)
query_result = cursor.fetchall()
for i in query_result:
    print(i)



sql_command = """INSERT INTO USER VALUES('user1', 'pass1', 0, 1000, False);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO USER VALUES('user2', 'pass2', 250, 1700, False);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO USER VALUES('user3', 'pass3', 10000, 15000, True);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO USER VALUES('user4', 'pass4', -750, 0, False);"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO USER VALUES('user5', 'pass5', 300, 1300, False);"""
#cursor.execute(sql_command)

sql_command = """UPDATE USER
SET BALANCE = 1000 WHERE USERID = 'user1'
"""
#cursor.execute(sql_command)

sql_command = """INSERT INTO ADMIN VALUES('admin1', 'apass1');"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO ADMIN VALUES('admin2', 'apass2');"""
#cursor.execute(sql_command)
sql_command = """INSERT INTO ADMIN VALUES('admin3', 'apass3');"""
#cursor.execute(sql_command)

sql_command = """ALTER TABLE GAMES
ADD WINS INT NOT NULL DEFAULT(0)
"""
#cursor.execute(sql_command)

sql_command = """ALTER TABLE GAMES
ADD LOSSES INT NOT NULL DEFAULT(0)
"""
#cursor.execute(sql_command)

sql_command = """INSERT INTO HISTORY VALUES('2024-07-11-08:31:44', 'Slots', 'user4', 'Loss','750')"""
cursor.execute(sql_command)
sql_command = """INSERT INTO HISTORY VALUES('2024-07-11-09:23:26', 'Craps', 'user2', 'Win','250')"""
cursor.execute(sql_command)

database.commit()
database.close()