# server_version.py - retrieve and display database server version

import MySQLdb

conn = MySQLdb.connect (host = "localhost",
		   user = "root",
		   passwd = "wpxk00",
		   db = "test")
cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone ()
print "server version:", row[0]
cursor.close ()
conn.close ()


#!/usr/bin/python
# import MySQL module
# connect
db = MySQLdb.connect(host="localhost", user="root", passwd="wpxk00",
		db="test")
# create a cursor
cursor = db.cursor()
# execute SQL statement
cursor.execute("SELECT * FROM animals")
# get the resultset as a tuple
result = cursor.fetchall()

print "====== %d rows ====" % (int(cursor.rowcount))

# iterate through resultset
for record in result:
	print record[0] , "-->", record[1]
print "="*30

# get user input
name = raw_input("Please enter a name: ")
species = raw_input("Please enter a species: ")

# execute SQL statement
cursor.execute("INSERT INTO animals (name, species) VALUES (%s, %s)",
		(name, species))
print "====== %d rows ====" % (int(cursor.rowcount))
