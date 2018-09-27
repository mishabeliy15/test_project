import time
import telebot
from telebot import types
from my_parser import *
import youtube_dl
import os
import datetime
from UserBot import UserBot

token = "464958591:AAG6_2iK9BePRuWyMvCg5vejzixlunfNz64"
bot = telebot.TeleBot(token)

N = 8 #Count of request
working = []
users = {}

@bot.message_handler(commands=['start', 'help'])
def command_help(message):
    pass

@bot.message_handler(content_types=['text'])
def handle_text(message):
    id_ch = message.chat.id
    user = users.get(id_ch)
    if (id_ch not in working) and (user == None or user.update(5)):
        if user == None:
            users[id_ch] = UserBot(id_ch)
            user = users[id_ch]
        working.append(message.chat.id)
        if valid_url(message.text):
            link = message.text
            bot.send_message(message.chat.id, "Your video in processing. Don't try flood! Your all requests ignore, while processing.")
            mp3(link, message)
        elif valid_req(message.text):
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
        working.remove(message.chat.id)
        user.update(5)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    url = str(call.data)
    user = users.get(call.message.chat.id)
    if (url != '' and call.message.chat.id not in working) and (user == None or user.update(10)):
        working.append(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Your video in processing. Don't try flood! Your all requests ignore, while processing.")
        mp3(url, call.message, parse_name=True)
        working.remove(call.message.chat.id)
        if user == None:
            users[call.message.chat.id] = UserBot(call.message.chat.id)
        else:
            user.update(5)


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

def valid_url(url):
    f = False
    temp1 = url.split("https://www.")
    if len(temp1) > 1 and temp1[1].find(".com/watch?v=") != -1:
        f = True
    return f

def valid_req(s):
    f = False
    for i in range(len(s)):
        temp = ord(s.lower()[i])
        if (temp >= 97 and temp <= 122) or (temp >= 1072 and temp <= 1103):
            f = True
            break
    return f

count = 0
while True:
    try:
        count += 1
        bot.polling(none_stop=True)
    except Exception as e:
        logging(str(count) + " | " + str(e))
        time.sleep(10)
