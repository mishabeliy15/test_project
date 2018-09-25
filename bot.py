import time

import telebot
from telebot import types
from my_parser import *
import youtube_dl
import os
import datetime

token = ""
bot = telebot.TeleBot(token)

N = 8 #Count of request
working = []

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.split("//")[0] == ("https:" or "http:"):
        link = message.text
        mp3(link, message)
    else:
        parse = Parsing(message.text)
        inlineKey = types.InlineKeyboardMarkup()
        row = []
        n = N if N <= len(parse.videos) else len(parse.videos)
        for i in range(n):
            print("[" + parse.req_search + " | " + parse.videos[i].name + "] " + parse.videos[i].url)
            callback_button = types.InlineKeyboardButton(text=str(i + 1), callback_data=parse.videos[i].url)
            row.append(callback_button)
        inlineKey.row(*row)
        bot.send_message(message.chat.id, parse.get_names_to_str(n), reply_markup=inlineKey)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    url = str(call.data)
    if url != '' and url not in working:
        working.append(url)
        mp3(url, call.message, parse_name=True)
        working.remove(url)


def mp3(link, message, parse_name=True):
    name = get_name(link) if parse_name else "temp"
    download_mp3_from_video(link, name)
    audi = open(name + ".mp3", 'rb')
    bot.send_audio(message.chat.id, audi)
    audi.close()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name + '.mp3')
    os.remove(path)

def download_mp3_from_video(url, name):
    outtmpl = name + '.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', },
            {'key': 'FFmpegMetadata'},
        ],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def logging(str):
    now = datetime.datetime.now()
    filename = now.date().__str__() + ".log"
    f = open(filename, "a")
    temp_str = "[{0}] {1}\n".format(now.today(), str)
    f.write(temp_str)
    f.close()

count = 0
while True:
    try:
        count += 1
        bot.polling()
    except Exception as e:
        logging(str(count) + " | " + str(e))
        bot.stop_polling()
        time.sleep(15)
