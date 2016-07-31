import sqlite3 as db

CREATE_1 = """
CREATE TABLE TOPGROSSING(
generateDate DATE NOT NULL,
rank INT NOT NULL, 
title TEXT,
price INT,
publisher TEXT,
category TEXT,
description TEXT,
download TEXT,
inAppProducts TEXT,
lastUpdate TEXT,
size TEXT,
rate REAL
)
"""

CREATE_2 = """
CREATE TABLE TOPPAID(
generateDate DATE NOT NULL,
rank INT NOT NULL, 
title TEXT,
price INT,
publisher TEXT,
category TEXT,
description TEXT,
download TEXT,
inAppProducts TEXT,
lastUpdate TEXT,
size TEXT,
rate REAL
)
"""
CREATE_3 = """
CREATE TABLE TOPFREE(
generateDate DATE NOT NULL,
rank INT NOT NULL, 
title TEXT,
price INT,
publisher TEXT,
category TEXT,
description TEXT,
download TEXT,
inAppProducts TEXT,
lastUpdate TEXT,
size TEXT,
rate REAL
)

"""

CONN = db.connect('appdata.db')
CONN.execute(CREATE_1)
CONN.execute(CREATE_2)
CONN.execute(CREATE_3)
CONN.commit()
CONN.close()
# SQL = """
# SELECT * FROM TOPGROSSING WHERE rank == 1
# """
# cursor = conn.cursor()
# cursor.execute(SQL)

# print(cursor.fetchall())


# conn.close()
