import telebot
from telebot import types
from my_parser import *
import youtube_dl
import os

token = "541246088:AAFL0Ph2TE8iiCVFq9Io2zhFXhUjZrcj9tQ"
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


def download_mp3_from_video(url,name):
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

def mp3_video(video, message): #Вместо урла принимает объект класса Video with name and url
    download_mp3_from_video(video.url, video.name)
    audi = open(video.name + ".mp3", 'rb')
    bot.send_audio(message.chat.id, audi)
    audi.close()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), video.name + '.mp3')
    os.remove(path)

def mp3(link, message):
    name = get_name(link)
    download_mp3_from_video(link, name)
    audi = open(name + ".mp3", 'rb')
    bot.send_chat_action(message.from_user.id, 'upload_audio')
    bot.send_audio(message.from_user.id, audi)
    audi.close()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name + '.mp3')
    os.remove(path)



bot.polling(none_stop=True)