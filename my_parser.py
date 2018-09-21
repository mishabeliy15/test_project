from bs4 import BeautifulSoup
import requests


class Parsing:
    youtube_search = 'https://www.youtube.com/results?sp=EgIQAQ%253D%253D&search_query='

    def __init__(self, req):
        self.req_search = req
        self.site = BeautifulSoup(self.gethtml(self.youtube_search + req), 'lxml')
        self.videos = []
        self.parsing_videos()
        self.to_videos()

    def gethtml(self, url):
        r = requests.get(url)
        return r.text

    def parsing_videos(self):
        self.blocks_a = self.site.select(
            'a[class*="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"]')
        self.times_span = self.site.select('span[class="accessible-description"]')


    def get_names_to_str(self, n):
        s = ''
        count = 0
        for i in self.videos:
            count += 1
            s += str(count) + ") " + i.name + " | " + str(round(i.time_s / 60, 2)) + " min.""\n"
            if count == n:
                break
        return s

    def to_videos(self):
        j = 0
        for i in range(len(self.blocks_a)):
            temp = Video(self.blocks_a[i], self.times_span[j])
            if (len(temp.url) < 100) and (temp.time_s < 60*50):
                self.videos.append(temp)
            if j + 1 < len(self.times_span):
                j += 1


youtube = 'https://www.youtube.com'


class Video():
    def __init__(self, soup,soup_t):
        self.name = soup.text
        self.url = youtube + soup.attrs['href']
        temp = soup_t.text.split(':')
        time = 0
        i = len(temp) - 1
        temp[i] = temp[i][0:len(temp[i]) - 1]
        multiple = 1
        while i > 0:
            time += int(temp[i])*multiple
            multiple *= 60
            i -= 1
        self.time_s = time

    def __str__(self):
        return self.name + " | " + str(round(self.time_s / 60)) + "min."


def get_name(url):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    name = soup.select('span[class*="watch-title"]')
    name = name[0].attrs['title'].lower().replace(',', '_').replace('.', '_').replace(' ', '_').replace('-',
                                                                                                        '_').replace('#', '')
    name = name.replace('|','_')

    return name
