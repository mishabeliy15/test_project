from bs4 import BeautifulSoup
import requests


class Parsing:
    youtube = 'https://www.youtube.com/results?search_query='
    def __init__(self, req):
        self.req_search = req
        self.site = BeautifulSoup(self.gethtml(self.youtube + req),'lxml')

    def gethtml(self, url):
        r = requests.get(url)
        return r.text
    def parsing_videos(self):
        self.blocks_a = self.site.find_all('a', {'class': 'yt-uix-tile-link'})

    def get_all_name_to_str(self):
        s = ''
        for i in self.blocks_a:
            s += i.text
