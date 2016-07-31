#-*- encoding: utf-8 -*-
from GoogleRankAPI import *
from AppInfo import *
import csv
import time
import datetime
import sqlite3
from multiprocessing.pool import ThreadPool

def toCSV(app_list, fileName):
    with open(fileName, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quoting = csv.QUOTE_NONE)
        columns = ['rank', 'title', 'price', 'publisher', 'category', 'description', 'download', 'inAppProducts', 'lastUpdate', 'size', 'rate']
        writer.writerow(columns)
        for x in app_list:            
            try:
                writer.writerow(x)
            except:
                print(x)
    print('%s complete' % fileName)

def GetAppInfo(DATA):
    info = []
    rank, title, link = DATA
    thisApp = AppInfo(link)
    info = thisApp.getInfo()
    info.insert(0, rank)
    info.insert(0, datetime.date.today())
    #print(info[1], info[2])
    return info

def ToSQLite(table, data):
    SQL = "INSERT INTO " + table + '''
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect('appdata.db')
    try:
        conn.executemany(SQL, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def getData(URL):
    API = GoogleRankAPI(URL)
    API.GetInfo()
    DATA = API.GetList()
    # DATA = [['rank', 'title', link']]
    pool = ThreadPool(processes = 16)
    async_result = pool.map_async(GetAppInfo, DATA)
    result = async_result.get()

    return result

if __name__=='__main__':
    beginTime = datetime.datetime.now()
    topGrossingURL = "https://play.google.com/store/apps/category/GAME/collection/topgrossing"
    topSellingFreeURL = "https://play.google.com/store/apps/category/GAME/collection/topselling_free"
    topSellingPaidURL = "https://play.google.com/store/apps/category/GAME/collection/topselling_paid"
    topSellingNewFreeURL = "https://play.google.com/store/apps/category/GAME/collection/topselling_new_free"
    
    today = time.strftime('%Y%m%d')

    print("최고 매출-게임 순위 읽는 중")
    topGrossingData = getData(topGrossingURL)
    print("추출 완료")
    ToSQLite("TOPGROSSING", topGrossingData)
    toCSV(topGrossingData, "raw/topGrossing_" + today + ".tsv")

    print("인기 게임 순위 읽는 중")
    topSellingFreeData = getData(topSellingFreeURL)
    print("추출 완료")    
    ToSQLite("TOPFREE", topSellingFreeData)
    toCSV(topSellingFreeData, "raw/topFree" + today + ".tsv")

    print("인기 유료 게임 순위 읽는 중")
    topSellingPaidData = getData(topSellingPaidURL)
    print("추출 완료")    
    ToSQLite("TOPPAID", topSellingPaidData)
    toCSV(topSellingPaidData, "raw/topPaid" + today + ".tsv")

    endTime = datetime.datetime.now()
    timeDiff = endTime - beginTime
    print("Execute Time: %s" % timeDiff)
    input("Press Enter to continue...")