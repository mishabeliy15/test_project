from bs4 import BeautifulSoup
import requests

class Parsing:
    youtube = 'https://www.youtube.com/results?search_query='
    def __init__(self, req):
        self.req_search = req
        self.site = BeautifulSoup(self.gethtml(self.youtube + req),'lxml')
        self.parsing_videos()
        self.toVideos()

    def gethtml(self, url):
        r = requests.get(url)
        return r.text

    def parsing_videos(self):
        self.blocks_a = self.site.find_all('a', {'class': 'yt-uix-tile-link'})

    def get_all_name_to_str(self):
        s = ''
        for i in self.blocks_a:
            s += i.text + "\n"
        return s

    def toVideos(self):
        self.videos = []
        for i in self.blocks_a:
            self.videos.append(Video(i))

class Video:
    def __init__(self,soup):
        self.soup = soup
        self.name = soup.text
        self.url = 'https://www.youtube.com/'+ soup.attrs['href']

    def __str__(self):
        return self.name
