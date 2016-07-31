import pandas as pd
import sqlite3 as db


fileList = ["raw/topFree_20160613.tsv", "raw/topGrossing_20160613.tsv","raw/topPaid_20160613.tsv"]
tableList = ["topFree", "topGrossing", "topPaid"]

INSERT_SQL = '''
INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
CHECK_SQL = '''
SELECT DISTINCT GENERATEDATE FROM %s
'''
conn = db.connect('appdata.db')
cursor = conn.cursor()
for file, table in zip(fileList, tableList):
	temp = pd.read_table(fileList[0], sep="\t")
	tempList = temp.as_matrix()
	print(tempList)	
	cursor.executemany(INSERT_SQL % tableList[0], tempList)
	cursor.execute(CHECK_SQL % tableList[0])
	print(cursor.fetchall())

conn.commit()
conn.close()