import telebot
import config
import test_database as database

bot = telebot.TeleBot(config.token)


def create_markup(t):
    m = telebot.types.InlineKeyboardMarkup()
    for b in t:
        m.add(telebot.types.InlineKeyboardButton(b[0], callback_data=b[1]))
    return m


def send_img(user_id, img_name, markup):
    with open("img\\" + img_name + ".png", 'rb') as photo:
        bot.send_photo(user_id, photo, config.texts[img_name], reply_markup=markup)


def moving(call, updown):
    user_pr = database.get_progress(call.from_user.id)
    coord = user_pr.split("_")
    if updown:
        update = str(int(coord[0]) + int(call.data.split("_")[0])) + "_" + coord[1]
    else:
        update = coord[0] + "_" + str(int(coord[1]) + int(call.data.split("_")[2]))
    if user_pr == "1_0":
        update += "_0"
    database.update_progress(call.from_user.id, update)
    send_img(call.from_user.id, update, create_markup(config.marks[update]))


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    start_game = telebot.types.InlineKeyboardButton("\U0001F3AE Начать игру", callback_data="start game")
    about_game = telebot.types.InlineKeyboardButton("\U00002754 Информация об игре", callback_data="about")
    markup.add(start_game, about_game)
    bot.send_message(message.from_user.id, config.start_mes, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.message.content_type == 'text':
        bot.edit_message_text(call.message.text, call.from_user.id, call.message.message_id)
    elif call.message.content_type == 'photo':
        bot.edit_message_caption(call.message.caption, call.from_user.id, call.message.message_id)

    if call.data == "start game":
        ind = database.add_player(call.from_user.id, call.from_user.first_name)
        send_img(call.from_user.id, ind, create_markup(config.marks[ind]))
    elif call.data == "about":
        ab_markup = telebot.types.InlineKeyboardMarkup()
        ab_markup.add(telebot.types.InlineKeyboardButton("\U0001F3AE Начать игру", callback_data="start game"))
        bot.send_message(call.from_user.id, config.about, reply_markup=ab_markup)
    elif "info" in call.data:
        u_p = call.data.split(" ")[1]
        bot.send_message(call.from_user.id, config.explore[u_p], reply_markup=create_markup(config.marks[u_p][1:]))
    elif "add" in call.data:
        data_arr = call.data.split(" ")
        database.add_to_events(call.from_user.id, data_arr[1])
        send_img(call.from_user.id, data_arr[2], create_markup(config.marks[data_arr[2]]))
    elif "_" in call.data:
        if call.data[0] != "_":
            moving(call, True)
        else:
            moving(call, False)
    elif call.data == "door":
        user_pr = database.get_progress(call.from_user.id)
        if user_pr == "1_0":
            send_img(call.from_user.id, "1_0_0", create_markup(config.marks["1_0_0"]))
        elif user_pr == "2_-2":
            bot.send_message(call.from_user.id, config.no_exit, reply_markup=create_markup(config.marks[user_pr][1:]))
    elif call.data == "read note":
        user_pr = database.get_progress(call.from_user.id)
        if user_pr == "2_0_0":
            database.update_progress(call.from_user.id, "2_0_1")
            send_img(call.from_user.id, "note_1", create_markup(config.marks["note"]))
    elif call.data == "drop note" or call.data == "return":
        user_pr = database.get_progress(call.from_user.id)
        send_img(call.from_user.id, user_pr, create_markup(config.marks[user_pr]))
    else:
        events_arr = database.get_events(call.from_user.id).split("_")
        if call.data not in events_arr:
            send_img(call.from_user.id, call.data, create_markup(config.marks[call.data]))
        else:
            not_event = "not_" + call.data
            send_img(call.from_user.id, not_event, create_markup(config.marks[not_event]))


if __name__ == "__main__":
    bot.polling(none_stop=True)
