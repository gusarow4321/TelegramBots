import telebot

bot = telebot.TeleBot("600150670:AAEvKgOCOBHBZ9NLzF4XWZft_xF2x6Q9tRU")

users_arr = dict()

keyb = telebot.types.InlineKeyboardMarkup()
button_plus = telebot.types.InlineKeyboardButton(text='+', callback_data='1')
button_minus = telebot.types.InlineKeyboardButton(text='-', callback_data='0')
keyb.add(button_plus, button_minus)

t = []
with open('1.txt', 'r') as file:
    for row in file.readlines():
        t.append(row.strip())


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, text='Тест будет состоять из четырех блоков, в каждом из которых по 20 '
                                                'свойств, характерных для представителей каждого типа '
                                                'темперамента.\n\nВнимательно прочитайте каждое свойство и поставьте '
                                                'знак (+), если считаете, что это свойство Вам присуще, и знак (–) – '
                                                'если оно у Вас отсутствует\n\nОтправьте /continue когда будете готовы')


@bot.message_handler(commands=['continue'])
def test_handler(message):
    users_arr[message.from_user.id] = [0, 0, 0, 0]
    bot.send_message(message.from_user.id, t[0], reply_markup=keyb)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    ind = t.index(call.message.text) + 1
    data = call.data
    type_temp = call.message.text.split('.')[0]
    users_arr[call.from_user.id][int(type_temp) - 1] += int(data)
    try:
        bot.edit_message_text(t[ind], call.from_user.id, message_id=call.message.message_id, reply_markup=keyb)
    except IndexError:
        h = round((users_arr[call.from_user.id][0] / sum(users_arr[call.from_user.id])) * 100)
        s = round((users_arr[call.from_user.id][1] / sum(users_arr[call.from_user.id])) * 100)
        f = round((users_arr[call.from_user.id][2] / sum(users_arr[call.from_user.id])) * 100)
        m = round((users_arr[call.from_user.id][3] / sum(users_arr[call.from_user.id])) * 100)
        mes = 'Результаты теста показывают, что ваш темперамент на {}% – холерический, {}% – сангвинический, ' \
              '{}% – флегматический и {}% – меланхолический.\n\n• Если относительный результат числа положительных ' \
              'ответов по какому-либо типу составляет 40% и выше, значит, данный тип темперамента у вас ' \
              'доминирующий.\n• Если этот результат составляет 30–39%, то качества данного типа выражены достаточно ' \
              'ярко.\n• Если результат 20–29%, то средне выражены.\n• При результате 10–19% можно утверждать, ' \
              'что черты этого типа темперамента выражены в малой степени.\n\nДля повторного прохождения теста ' \
              'отправьте /continue'.format(str(h), str(s), str(f), str(m))
        bot.edit_message_text(mes, call.from_user.id, message_id=call.message.message_id)
        del users_arr[call.from_user.id]


bot.polling(none_stop=True)
