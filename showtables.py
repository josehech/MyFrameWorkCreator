#!/usr/bin/python3

import sqlite3 as dbapi
import sys

# Colores
green = "\033[1;32m"
red = "\033[1;31m"

# BBDD
bbdd = dbapi.connect("bbdd.dat")
c = bbdd.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
sys.stdout.write(green)
for table in c.fetchall():
    print(table[0])
c.close()
bbdd.close()
