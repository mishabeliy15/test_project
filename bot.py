import telebot
from telebot import types
from my_parser import *
import youtube_dl
import os

token = ""
bot = telebot.TeleBot(token)

parse = None
inlineKey = None


@bot.message_handler(content_types=['text'])
def handle_text(message):
    '''if message.text == ('1' or '2' or '3' or '4' or '5'):
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'thx 4r choose', reply_markup=hide_markup)'''

    if message.text.split("//")[0] == ("https:" or "http:"):
        link = message.text
        mp3(link, message)
    else:
        global parse, inlineKey
        parse = Parsing(message.text)
        inlineKey = types.InlineKeyboardMarkup()
        row = []
        for i in range(5):
            callback_button = types.InlineKeyboardButton(text=str(i + 1), callback_data=str(i))
            row.append(callback_button)
        inlineKey.row(*row)

        bot.send_message(message.chat.id, parse.get_names_to_str(5),reply_markup=inlineKey)
        '''bot.send_message(message.chat.id, "Choose one...", reply_markup=inlineKey)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('1', '2', '3', '4', '5')
        bot.send_message(message.chat.id, 'Choose one...', reply_markup=user_markup)'''

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    i = int(call.data)
    if parse != None:
        mp3_video(parse.videos[i], call.message)

def mp3_video(video, message): #Вместо урла принимает объект класса Video with name and url
    name = video.name
    options = {
    'format': 'bestaudio/best',
    'outtmpl': name + '.mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video.url])
    audi = open(name + ".mp3", 'rb')
    #bot.send_chat_action(message.chat.id, 'upload_audio')
    bot.send_audio(message.chat.id, audi)
    audi.close()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name + '.mp3')
    os.remove(path)

def mp3(link, message):
    name = get_name(link)
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': name + '.mp3',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([link])
    audi = open(name + ".mp3", 'rb')
    bot.send_chat_action(message.from_user.id, 'upload_audio')
    bot.send_audio(message.from_user.id, audi)
    audi.close()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name + '.mp3')
    os.remove(path)



bot.polling(none_stop=True)