#-*- encoding: utf-8 -*-
#Top Grossing 주소
# https://play.google.com/store/apps/category/GAME/collection/topgrossing
import bs4 
import urllib
import csv
from selenium import webdriver
import re


rankRe = re.compile(r'\d+')
rateRe = re.compile(r'(\d\.\d)')
baseURL = "https://play.google.com"
topURL = "https://play.google.com/store/apps/top"
topGrossingURL = "https://play.google.com/store/apps/category/GAME/collection/topgrossing"

class GooglePlay:
    def getSite(self, URL):
        self.page = urllib.request.urlopen(URL)
        self.html = bs4.BeautifulSoup(self.page, 'html.parser')
    # 1위부터 x 위까지 순위 획득 
    def getInfo(self):
        self.titleList = self.html.find_all('a', class_='title')
        self.scoreList = self.html.find_all('div', class_='tiny-star star-rating-non-editable-container')
        self.resultList = []
        for x, y in zip(self.titleList, self.scoreList):
            title = x.get_text().replace('"', '').strip()
            link = baseURL + x.get('href').replace('"', '').strip()
            rate = y.get('aria-label').replace('"', '').strip()
            rank = rankRe.findall(title)
            rate = rankRe.findall(rate)
            title = rankRe.sub('', title).replace('"','').replace("'",'').replace('.', '').strip()
            self.resultList.append([rank[0], title, link, rate[1]+'.'+rate[2]])
    



if __name__ == '__main__':
    API = GooglePlay()
    API.getSite(topGrossingURL)
    API.getInfo()
    API.toCSV('list.csv')