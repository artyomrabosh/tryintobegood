import telebot
import datetime
import config
import sqlite3
import random
import schedule
from commands import kakoysegodnyaprazdnik, main, update_timetable

buttons = ['/lesson', '/time', '/kakoysegodnyaprazdnik?', '/wannaslide', "/github"]
bot = telebot.TeleBot(config.TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row('/lesson', '/time', '/kakoysegodnyaprazdnik?', '/wannaslide')
group = 'blank'
db = sqlite3.connect("users.db", check_same_thread=False)
sql = db.cursor()

keyboard = telebot.types.InlineKeyboardMarkup()
for button in buttons:
    keyboard.add(telebot.types.InlineKeyboardButton(text=button, callback_data=button))

schedule.every(3).days.do(update_timetable.update_timetable())    # раз в 3 дня обновляет расписание


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id=message.from_user.id
    sql.execute("""SELECT user_id FROM users""")        # проверка на регистрациб
    for item in sql.fetchall():
        if item == ('{}'.format(user_id),):
            print("success")
            bot.send_message(message.chat.id, 'youre logged', reply_markup=keyboard)
            return
    send = bot.send_message(message.chat.id, 'to login use group number (example 102/1)', reply_markup=keyboard)
    bot.register_next_step_handler(send, register)


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.from_user.id, "Вот что я умею", reply_markup=keyboard)


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


def timing(message):
    timer = '{}'.format(datetime.datetime.utcnow() + datetime.timedelta(hours=3))
    print(timer)
    bot.send_message(message.chat.id, 'time: {}'.format(timer[:-10]))


def holidays(message):
    holidays = kakoysegodnyaprazdnik.get_holidays()
    for day in holidays:
        bot.send_message(message, day)
    bot.send_message(message, "incredible", reply_markup=keyboard)

@bot.message_handler(commands=['wannaslide'])
def slides(message):
    slide = "slides/00{}{}.jpg".format(random.randrange(0,2), random.randrange(0,9))
    f = open(slide, 'rb')
    bot.send_photo(message, f)
    bot.send_message(message, "incredible", reply_markup=keyboard)


def git(message):
    print(message)
    markup = telebot.types.InlineKeyboardMarkup()
    users = ["artyomrabosh", "OcTatiana", "alexarlord-boop", "Vasis3038"]
    print("hi")
    for user in users:
        markup.add(telebot.types.InlineKeyboardButton(text=user, callback_data="info " + user))
    bot.send_message(message, "ВЫБЕРИТЕ КНОПКУ", reply_markup=markup)


def lesson(message):
    answer = []
    user_id = message
    for item in sql.execute("""SELECT * FROM users"""):
        if item[0] == user_id:             # смотрим группу пользователя
            answer = main.main(item[1])
            break
    for item in answer:
        if item != "":
            if item is not None:
                bot.send_message(message, item)
            else:
                bot.send_message(message, 'no lessons :)')
    bot.send_message(message, "incredible", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda a:True)
def inline(a):
    user_id = a.from_user.id
    if a.data.split(" ")[0] == 'get_pulls':
        pulls = github.get_pulls(a.data.split(" ")[1])
        for pull in pulls[:7]:
            bot.send_message(user_id, pull['title'])
        bot.send_message(user_id, "incredible", reply_markup=keyboard)

    elif a.data.split(" ")[0]== 'info':
        print(a.data)
        markup = telebot.types.InlineKeyboardMarkup()
        get_pulls_btn = telebot.types.InlineKeyboardButton(text='get pulls', callback_data='get_pulls '+a.data.split(" ")[1])
        markup.add(get_pulls_btn)
        bot.send_message(user_id, "Пампам", reply_markup=markup)
    elif a.data == "/time":
        timing(user_id)
    elif a.data == '/lesson':
        lesson(user_id)
    elif a.data == '/kakoysegodnyaprazdnik?':
        holidays(user_id)
    elif a.data == '/wannaslide':
        slides(user_id)
    elif a.data == '/github':
        git(user_id)


bot.polling()
