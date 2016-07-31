import datetime
import time
import sqlite3 as db

conn = db.connect(':memory:')#detect_types=db.PARSE_DECLTYPES | db.PARSE_COLNAMES)
now = datetime.date.today()
print(now)
conn.execute("CREATE TABLE TEMP(NOW DATE)")
conn.execute("INSERT INTO TEMP VALUES(?)", (now,))
c = conn.cursor()
c.execute("SELECT * FROM TEMP")
print(c.fetchall())

conn.close()

#print(time.strftime('%Y-%m-%d'))
