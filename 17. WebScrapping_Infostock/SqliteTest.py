# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
import time

connect = sqlite3.connect('InfoStock.db')
cursor = connect.cursor()

cursor.execute('SELECT * FROM INFOSTOCK ')
for row in cursor:
    print ('%s %s %s' % ( row[0], row[1], row[2]) )