#!/usr/bin/python3
import sqlite3 as dbapi
import sys

# Colores
green = "\033[1;32m"
red = "\033[1;31m"

# BBDD
bbdd = dbapi.connect("bbdd.dat")
c = bbdd.cursor()
c.execute('SELECT * FROM '+ sys.argv[1])
entry = c.fetchall()
for comando in entry:
	sys.stdout.write(red)
	print(comando[0:3])
	sys.stdout.write(green)
	print(comando[3])
c.close()
bbdd.close()
