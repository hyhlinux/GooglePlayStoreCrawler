#-*- encoding: utf-8 -*-
import bs4
import re
from urllib.request import urlopen


#from urllib import urlopen


rateStarRE = re.compile(r'\d\.\d')

def removeHTMLTag(text):
    try:
        text = text.get_text(strip=True).replace('"', ' ').replace(',', ' ').replace('\t', ' ').strip()
        text = re.sub(' +', ' ', text)
        return text
    except:
        return 'NA'
def priceToInt(text):
    if type(text) == int:
        return text
    else: 
        return text.replace(u'₩', '').replace(',','').strip()
class AppInfo:
    def __init__(self, URL):
        PAGE = urlopen(URL)
        self.HTML = bs4.BeautifulSoup(PAGE, 'html.parser')

    def getInfo(self):        
        title = self.HTML.find('div', class_='id-app-title')
        publisher = self.HTML.find('span', attrs={'itemprop':'name'})
        category = self.HTML.find('span', attrs={'itemprop':'genre'})
        description = self.HTML.find('div', attrs={'itemprop': 'description'})
        download = self.HTML.find('div', attrs={'itemprop': 'numDownloads'})
        try:
            inAppProducts = self.HTML.find(name='div', class_='title', text=u"인앱 상품").findNext('div')
        except:
            inAppProducts = 'NA'
        try:
            lastUpdate = self.HTML.find(name='div', class_='title', text=u"업데이트 날짜").findNext('div')
        except:
            lastUpdate = 'NA'
        try:
            price = self.HTML.find(name='meta', attrs={'itemprop':'price'}).get('content')
        except:
            price = 0
        size = self.HTML.find('div', attrs={'itemprop':'fileSize'})        
        try:
            rate = self.HTML.find('div', class_='tiny-star star-rating-non-editable-container').get('aria-label')
            rate = rateStarRE.findall(rate)[0]
        except:
        	rate = 0.0
        #title, price, publisher, category, description, download, inAppProducts, lastUpdate, size, rate
        self.List = [title, publisher, category, description, download, inAppProducts, lastUpdate, size]
        self.List = [removeHTMLTag(x) for x in self.List]               
        self.List.insert(1, priceToInt(price))
        self.List.append(float(rate))
        return (self.List) 

if __name__ == '__main__':
    testURL = "https://play.google.com/store/apps/details?id=com.epicwaronline.ms"
    paidTestURL = "https://play.google.com/store/apps/details?id=com.mojang.minecraftpe"
    T_URL = "https://play.google.com/store/apps/details?id=com.ekkorr.endlessfrontier"
    main = AppInfo(paidTestURL)
    print(main.getInfo())

