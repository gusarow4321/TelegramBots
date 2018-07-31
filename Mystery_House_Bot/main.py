import telebot
import config
import database

bot = telebot.TeleBot(config.token)


def send_img(user_id, img_name):
    with open("img\\" + img_name + ".png", 'rb') as photo:
        bot.send_photo(user_id, photo, config.texts[img_name])


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    start_game = telebot.types.InlineKeyboardButton("\U0001F3AE Начать игру", callback_data="start game")
    about_game = telebot.types.InlineKeyboardButton("\U00002754 Информация об игре", callback_data="about")
    markup.add(start_game, about_game)
    bot.send_message(message.from_user.id, config.start_mes, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "start game":
        database.add_player(call.from_user.id, call.from_user.first_name)
        send_img(call.from_user.id, database.get_img(call.from_user.id))

    elif call.data == "about":
        ab_markup = telebot.types.InlineKeyboardMarkup()
        ab_markup.add(telebot.types.InlineKeyboardButton("\U0001F3AE Начать игру", callback_data="start game"))
        bot.send_message(call.from_user.id, config.about, reply_markup=ab_markup)


if __name__ == "__main__":
    bot.polling(none_stop=True)
