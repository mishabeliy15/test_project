from bs4 import BeautifulSoup
import requests

class Parsing:
    youtube_search = 'https://www.youtube.com/results?sp=EgIQAQ%253D%253D&search_query='

    def __init__(self, req):
        self.req_search = req
        self.site = BeautifulSoup(self.gethtml(self.youtube_search + req),'lxml')
        self.videos = []
        self.parsing_videos()
        self.to_videos()

    def gethtml(self, url):
        r = requests.get(url)
        return r.text

    def parsing_videos(self):
        self.blocks_a = self.site.find_all('a', {'class': 'yt-uix-tile-link'})

    def get_names_to_str(self):
        s = ""
        count = 0
        for i in self.blocks_a:
            count += 1
            s += str(count) + ") " + i.text + "\n"
        return s

    def get_names_to_str(self, n):
        s = ''
        count = 0
        for i in self.blocks_a:
            count += 1
            s += str(count) + ") " + i.text + "\n"
            if count == n:
                break
        return s

    def to_videos(self):
        for i in self.blocks_a:
            self.videos.append(Video(i))

youtube = 'https://www.youtube.com'
class Video():
    def __init__(self,soup):
        self.name = soup.text
        self.url = youtube + soup.attrs['href']

    def __str__(self):
        return self.name

def get_name(url):
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    name = soup.select('span[class*="watch-title"]')
    return name[0].attrs['title']