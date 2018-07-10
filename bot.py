from config import token
import telebot
import random

bot = telebot.TeleBot(token)

players = {}


@bot.message_handler(commands=['start'])
def start_handler(message):
    print(message.from_user.first_name + ': ' + message.text)
    bot.send_message(message.from_user.id, "\U0001F3AE Game is started\nFor end a game send \stop")
    players[message.from_user.id] = {'name': message.from_user.first_name, 'score': 0}
    bot.send_message(message.from_user.id, 'Choose 5 numbers ranging from 1 to 20.\nFor example: 1 2 3 4 5')


@bot.message_handler(commands=['stop'])
def stop_handler(message):
    print(message.from_user.first_name + ': ' + message.text)
    bot.send_message(message.from_user.id, f'Game over\nYour final score: {players[message.from_user.id]["score"]}')
    del players[message.from_user.id]


@bot.message_handler(content_types=['text'])
def game(message):
    print(message.from_user.first_name + ': ' + message.text)
    if message.from_user.id in players:
        arr = [str(random.randrange(1, 21)) for i in range(5)]
        bot.send_message(message.from_user.id, 'Winning numbers: ' + ' '.join(arr))
        player_arr = message.text.split(' ')
        correct_nums = 0
        for val in arr:
            if val in player_arr:
                correct_nums += 1
        players[message.from_user.id]["score"] += correct_nums
        if correct_nums > 0:
            bot.send_message(message.from_user.id, f'\U0001F389 You guessed {correct_nums} numbers\n'
                                                   f'Your score is {players[message.from_user.id]["score"]}')
        else:
            bot.send_message(message.from_user.id, '\U0001F62D You lose')
    else:
        bot.send_message(message.from_user.id, 'Use command /start to start the game')


if __name__ == '__main__':
    bot.polling(none_stop=True)
