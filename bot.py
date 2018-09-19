from parser import Parsing
import telebot


token = ("541246088:AAFL0Ph2TE8iiCVFq9Io2zhFXhUjZrcj9tQ")

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    test = Parsing(message.text)
    test.parsing_videos()
    bot.send_message(message.chat.id, test.get_all_name_to_str())


bot.polling(none_stop=True)