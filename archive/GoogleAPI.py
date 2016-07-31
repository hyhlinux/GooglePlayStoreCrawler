#-*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import bs4
import re
import csv

rankRe = re.compile(r'\d+')
rateRe = re.compile(r'(\d\.\d)')
baseURL = "https://play.google.com"


class GoogleAPI:
    def __init__(self, driver):
        self.browser = webdriver.Chrome(driver)

    def getSite(self, URL):
        self.browser.get(URL)

    def scrollDown(self):
        state = False
        while state == False:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.1)
            self.browser.execute_script("window.scrollTo(0, 0);")
            showMoreButton = self.browser.find_element_by_id('show-more-button')            
            if showMoreButton.is_displayed():
                showMoreButton.click()
            titleList = self.browser.find_elements_by_xpath("//a[@class='title']")
            if (len(titleList)) == 540:
                state = True

    def getInfo(self):
        self.scrollDown()
        self.html = bs4.BeautifulSoup(self.browser.page_source, 'html.parser')
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
        self.close()

    def toCSV(self, fileName):
        with open(fileName, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([u'Rank', u'Title', u'Link', u'UserRate'])
            for x in self.resultList:
                writer.writerow(x)
        print('toCSV complete')

    def getList(self):
        return self.resultList

    def close(self):
        self.browser.quit()

if __name__=="__main__":
    topGrossingURL = "https://play.google.com/store/apps/category/GAME/collection/topgrossing"
    browser = GoogleAPI("webdriver/chromedriver.exe")
    browser.getSite(topGrossingURL)
    browser.scrollDown()
    browser.getInfo()
    browser.close()
    browser.toCSV("list.csv")
    