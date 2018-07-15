import telebot
import requests as req

bot = telebot.TeleBot(<token>)
token_openweathermap = <your token>  # токен для api погоды
w_dict = {'Thunderstorm': '\U000026A1', 'Drizzle': '\U00002601', 'Rain': '\U00002614', 'Snow': '\U00002744',
          'Clear': '\U00002600', 'Clouds': '\U000026C5'}


@bot.message_handler(commands=['start'])
def handler_start(message):
    bot.send_message(message.from_user.id, text='Привет, я бот и вот что я могу:\n\n1. Скажу погоду '
                                                'в Москве по команде /weather')


@bot.message_handler(commands=['weather'])
def handler_weather(message):
    r = req.get('https://api.openweathermap.org/data/2.5/weather?q=Moscow&lang=ru&appid=' + token_openweathermap).json()
    data = [w_dict[r["weather"][0]["main"]], r["weather"][0]["description"], str(int(r["main"]["temp"]) - 273),
            r["wind"]["speed"], r["main"]["humidity"]]
    bot.send_message(message.from_user.id,
                     text=f'Погода в Москве\n\n{data[0]}{data[1]}\n\U0001F321 Температура {data[2]}\U00002103 '
                          f'\n\U0001F4A8 Ветер {data[3]} м/c\n\U0001F4A7 Влажность {data[4]} %')


bot.polling(none_stop=True, interval=3)
