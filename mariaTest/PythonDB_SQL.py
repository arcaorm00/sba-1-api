import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='KlasseUser1', password='XXXXXX', database='pythondb')
cursor = mariadb_connection.cursor()

cursor.execute("INSERT INTO sampleTbl (ID, NAME) VALUES (%d, %s);", (1004, 'KlasseName'))
cursor.execute("SELECT * FROM sampleTbl;")
cursor.execute("UPDATE sampleTbl SET NAME = 'TEST' WHERE ID = 1004;")
cursor.execute("DELETE FROM sampleTbl WHERE ID = 1004;")
mariadb_connection.commit()

mariadb_connection.close()