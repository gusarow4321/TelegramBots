# Простой бот с ИИ
# пример взят отсюда: https://habr.com/post/346606/

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai
import json

updater = Updater(token='603647976:AAGb5fB67KDTm8_rKX96kCMyPQkMnZa1zho')

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет')


def text(bot, update):
    request = apiai.ApiAI('562c94ae1d1f4f26a58c28ce03ffb252').text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = update.message.text
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не понимаю!')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(text_handler)

updater.start_polling()
