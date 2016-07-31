"""Summary

Attributes:
    BASE_URL (str): Description
    RANK_RE (TYPE): Description
"""
import urllib
import urllib.parse
import urllib.request
import bs4
import re
BASE_URL = "https://play.google.com"
RANK_RE = re.compile(r'(\d+)\.')

class GoogleRankAPI:
	"""Summary
	Google 차트 순위 보여줌
	"""
	def __init__(self, URL):
		"""Summary
		
		Args:
		    URL (str): 구글 차트 사이트 주소
		"""
		self.URL = URL
		self.HEADERS = {
			"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
			"user-agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"	
		}
		self.titleList = []

	def ConnectRetreive(self, Params):
		"""Summary
		
		Args:
		    Params (JSON): Request POST 변수
		
		"""
		PARAMS = urllib.parse.urlencode(Params)
		BINARY_PARAMS = PARAMS.encode('utf-8')
		REQ = urllib.request.Request(self.URL, BINARY_PARAMS, self.HEADERS)
		RESPONSE = urllib.request.urlopen(REQ)

		HTML = bs4.BeautifulSoup(RESPONSE, 'html.parser')
		titleList = HTML.find_all(name='a', class_='title')
		#rank, title, link
		for item in titleList:
			title = item.get('title')
			link = BASE_URL + item.get('href')
			rank = int(RANK_RE.findall(item.get_text())[0])
			self.titleList.append([rank, title, link])

	def GetInfo(self):
		"""Summary
		정보 읽음

		"""
		PARAM_START = [0, 100, 200, 300, 400, 500]
		for x in PARAM_START:
			PARAMS = {
				"start": x,
				"num": 100
			}
			self.ConnectRetreive(PARAMS)

	def GetList(self):
		"""Summary
		
		Returns:
		    List: [rank, title, link] 형태의 리스트 반환
		"""
		return self.titleList

if __name__ == "__main__":
	URL = "https://play.google.com/store/apps/category/GAME/collection/topselling_free?authuser=0"
	GoogleAPI = GoogleRankAPI(URL)
	GoogleAPI.GetInfo()
	APP_LIST =  GoogleAPI.GetList()
	print(len(APP_LIST))
	print(APP_LIST)
