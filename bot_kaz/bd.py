import sqlite3
import time

# инициализация ботинка

def init_db():
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()


    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    tg_id INTEGER PRIMARY KEY,
    username TEXT,
    click_id TEXT,
    click_time INTEGER,
    access INTEGER DEFAULT 0
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS movies (
    code TEXT PRIMARY KEY,
    title TEXT
    )
    """)


    conn.commit()
    conn.close()

#добавление лида


#вытягиваем данные пользователя 

def get_user(tg_id):
    conn = sqlite3.connect("bot.db")
WHERE tg_id = ?", (tg_id,))
    user = c.fetchone()


    conn.close()
    return user

def unlock_access(tg_id):
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()

    c.execute("UPDATE users SET access = 1 WHERE tg_id = ?", (tg_id,))
    conn.commit()
    conn.close()



