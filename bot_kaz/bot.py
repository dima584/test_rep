import telebot
import uuid
import time
from bd import *
import sqlite3


TOKEN = "8423330553:AAHnba6WeQe7heoW5vmq-_8Eja8hQDkJ5Ns"
bot = telebot.TeleBot(TOKEN)


WAIT_TIME = 30 # 3 минуты ожидания
REF_LINK = "https://1wiojq.com/casino?p=ewav"


init_db()

@bot.message_handler(commands=['start'])
def start(msg):
    click_id = str(uuid.uuid4())[:8]


    add_user(
    msg.from_user.id,
    msg.from_user.username,
    click_id
    )


    link = f"{REF_LINK}&subid={click_id}"


    bot.send_message(
    msg.chat.id,
    f"🎰 Чтобы получить доступ к фильмам:\n\n"
    f"1️⃣ Зарегистрируйся по ссылке:\n{link}\n\n"
    f" По промокоду GGhardaxxx \n🔥 Бонус на первые депозиты + 500%\n🔥 500 ФРИСПИНОВ за первые четыре депозита\n\n"
    f"2️⃣ Вернись и нажми:\n"
    f"✅ /OK ✅"
    )

@bot.message_handler(commands=['done'])
def done(msg):
    user = get_user(msg.from_user.id)

    if not user:
        bot.send_message(msg.chat.id, "❌ Сначала нажми /start")
        return

    click_time, access = user

    

    passed = int(time.time()) - click_time

    if passed < WAIT_TIME:
        bot.send_message(
            msg.chat.id,
            "❌ Регистрация не подтверждена.\n"
            "Перейди по ссылке и зарегистрируйся."
        )
        return

    # прошло нужное время
    if passed >= WAIT_TIME:
        unlock_access(msg.from_user.id)
        bot.send_message(
            msg.chat.id,
            "✅ Регистрация подтверждена!\n"
            "Введи код фильма 🎬"
        
    )
        
@bot.message_handler(func=lambda m: True)
def movie(msg):
    user = get_user(msg.from_user.id)

    if not user or user[1] == 0:
        bot.send_message(
            msg.chat.id,
            "❌ Доступ закрыт. Зарегистрируйся и нажми /done"
        )
        return

    conn = sqlite3.connect("bot.db")
    c = conn.cursor()

    c.execute("SELECT title FROM movies WHERE code = ?", (msg.text,))
    movie = c.fetchone()
    conn.close()

    if movie:
        bot.send_message(msg.chat.id, f"🎬 Фильм: {movie[0]}")
    else:
        bot.send_message(msg.chat.id, "❌ Неверный код.")


bot.polling(none_stop=True)