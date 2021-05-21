import telebot
import datetime
import config
import sqlite3
import random
import schedule
from commands import kakoysegodnyaprazdnik, main, update_timetable


bot = telebot.TeleBot(config.TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row('/lesson', '/time', '/kakoysegodnyaprazdnik?', '/wannaslide')
group = 'blank'
db = sqlite3.connect("users.db", check_same_thread=False)
sql = db.cursor()

#schedule.every(3).days.do(update_timetable.update_timetable())    # раз в 3 дня обновляет расписание


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id=message.from_user.id
    sql.execute("""SELECT user_id FROM users""")        # проверка на регистрациб
    for item in sql.fetchall():
        if item == ('{}'.format(user_id),):
            print("success")
            bot.send_message(message.chat.id, 'youre logged' , reply_markup=keyboard)
            return
    send = bot.send_message(message.chat.id, 'to login use group number (example 102/1)', reply_markup = keyboard)
    bot.register_next_step_handler(send, register)


def register(message):
    global group
    print(message)
    user_id = message.from_user.id
    if message.text not in main.groups:
        bot.send_message(message.chat.id, 'wrong group number\n')
        start_message(message)
        return ''
    data = ("{}".format(user_id), message.text)
    sql.execute("""INSERT INTO users VALUES (?, ?);""", data)
    db.commit()
    bot.send_message(message.chat.id, 'to know what the lesson use /lesson\n', reply_markup = keyboard)


@bot.message_handler(commands=['time'])
def timing(message):
    timer = '{}'.format(datetime.datetime.utcnow() + datetime.timedelta(hours=3))
    print(timer)
    bot.send_message(message.chat.id, 'time: {}'.format(timer[:-10]))


@bot.message_handler(commands=['kakoysegodnyaprazdnik?'])
def holidays(message):
    holidays = kakoysegodnyaprazdnik.get_holidays()
    for day in holidays:
        bot.send_message(message.chat.id, day)

@bot.message_handler(commands=['wannaslide'])
def slides(message):
    slide = "slides/00{}{}.jpg".format(random.randrange(0,2), random.randrange(0,9))
    f = open(slide, 'rb')
    bot.send_photo(message.chat.id, f)
    print(slide)


@bot.message_handler(commands=['lesson'])
def lesson(message):
    answer = []
    user_id = message.from_user.id
    for item in sql.execute("""SELECT * FROM users"""):
        if item[0] == user_id:             # смотрим группу пользователя
            answer = main.main(item[1])
            break
    for item in answer:
        if item != "":
            if item is not None:
                bot.send_message(message.chat.id, item)
            else:
                bot.send_message(message.chat.id, 'no lessons :)')



bot.polling()
