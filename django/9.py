import asyncio
import sqlite3
import os
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link

# --- НАЛАШТУВАННЯ ---
genai.configure(api_key="AIzaSyDXQjiQErpgpIQPasv0rmCIdUPWfHOE9aQ")
model = genai.GenerativeModel('gemini-1.5-flash') 

TOKEN = "8245348261:AAHbsrMfbZum2JcTEXHss_lLjbhNmPSZnXQ"
ADMIN_ID = 983710534 
WELCOME_IMAGE_PATH = r"D:/django/.vs/VIRTUS FIT/photo_2026-02-10_00-37-24.jpg"
DB_NAME = 'virtus_ultimate_v11.db'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- БАЗА ДАНИХ ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        name TEXT, age INTEGER, weight REAL, goal TEXT, 
                        balance INTEGER DEFAULT 5,
                        referred_by INTEGER,
                        current_role TEXT DEFAULT 'coach')''')
    conn.commit(); conn.close()

class Registration(StatesGroup):
    waiting_for_name = State(); waiting_for_age = State()
    waiting_for_weight = State(); waiting_for_goal = State()

class Support(StatesGroup):
    waiting_for_bug_report = State()

# --- КЛАВІАТУРИ ---
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🏋️‍♂️ Тренування"), types.KeyboardButton(text="🍎 Харчування"))
    builder.row(types.KeyboardButton(text="💳 Баланс"), types.KeyboardButton(text="💬 Чат з AI"))
    builder.row(types.KeyboardButton(text="👤 Акаунт"), types.KeyboardButton(text="🆘 Підтримка"))
    builder.row(types.KeyboardButton(text="🔗 Рефералка"))
    return builder.as_markup(resize_keyboard=True)

def get_roles_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🏋️ Тренер", callback_data="set_role_coach"))
    builder.row(types.InlineKeyboardButton(text="🧠 Психолог", callback_data="set_role_psy"))
    builder.row(types.InlineKeyboardButton(text="🏥 Лікар-консультант", callback_data="set_role_doc"))
    return builder.as_markup()

# --- ОБРОБНИКИ СИСТЕМНИХ КНОПОК (Фікс) ---

@dp.message(F.text == "💬 Чат з AI") # ЦЬОГО БЛОКУ НЕ ВИСТАЧАЛО
async def ai_roles_menu(message: types.Message):
    await message.answer("Обери режим роботи ШІ асистента:", reply_markup=get_roles_keyboard())

@dp.message(F.text == "👤 Акаунт")
async def account_h(message: types.Message):
    conn = sqlite3.connect(DB_NAME)
    u = conn.execute("SELECT name, age, weight, goal, balance FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()
    conn.close()
    if u: await message.answer(f"👤 **Профіль**\nІм'я: {u[0]}\nВік: {u[1]}\nВага: {u[2]}кг\nЦіль: {u[3]}\n💳 Баланс: {u[4]} ⚡️")

@dp.message(F.text == "💳 Баланс")
async def balance_h(message: types.Message):
    conn = sqlite3.connect(DB_NAME)
    b = conn.execute("SELECT balance FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()
    conn.close()
    await message.answer(f"💰 Твій баланс: {b[0] if b else 0} ⚡️")

# --- РЕШТА ЛОГІКИ (СТАРТ, РЕЄСТРАЦІЯ, ШІ) ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    init_db()
    args = message.text.split()
    referrer = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    conn = sqlite3.connect(DB_NAME)
    user = conn.execute("SELECT user_id FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()
    if not user:
        conn.execute("INSERT INTO users (user_id, referred_by) VALUES (?, ?)", (message.from_user.id, referrer))
        conn.commit()
    conn.close()
    welcome_text = "👊 Привет! 👋😊 Добро пожаловать в Virtus."
    try: await message.answer_photo(photo=FSInputFile(WELCOME_IMAGE_PATH), caption=welcome_text, reply_markup=get_main_menu())
    except: await message.answer(welcome_text, reply_markup=get_main_menu())

@dp.callback_query(F.data.startswith("set_role_"))
async def set_role(callback: types.CallbackQuery):
    role = callback.data.split("_")[-1]
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE users SET current_role = ? WHERE user_id = ?", (role, callback.from_user.id))
    conn.commit(); conn.close()
    role_names = {"coach": "🏋️ Тренер", "psy": "🧠 Психолог", "doc": "🏥 Лікар"}
    await callback.message.answer(f"✅ Режим змінено на: {role_names[role]}. Тепер пиши або шлі голос!")
    await callback.answer()

@dp.message(F.text | F.voice)
async def handle_ai(message: types.Message):
    if message.text in ["🏋️‍♂️ Тренування", "🍎 Харчування", "💳 Баланс", "💬 Чат з AI", "👤 Акаунт", "🔗 Рефералка", "🆘 Підтримка"]:
        if message.text not in ["🏋️‍♂️ Тренування", "🍎 Харчування"]: return # Пропускаємо системні кнопки

    user_id = message.from_user.id; conn = sqlite3.connect(DB_NAME)
    user = conn.execute("SELECT name, balance, current_role FROM users WHERE user_id=?", (user_id,)).fetchone()
    if not user or user[1] <= 0:
        conn.close(); return await message.answer("❌ Недостатньо генерацій!")

    await message.answer("⏳ Обробка...")
    try:
        res = model.generate_content(f"Роль: {user[2]}. Запит: {message.text}")
        conn.execute("UPDATE users SET balance = balance - 1 WHERE user_id=?", (user_id,)); conn.commit()
        await message.answer(res.text)
    except Exception as e: await message.answer(f"Помилка: {str(e)}")
    finally: conn.close()

async def main(): init_db(); await dp.start_polling(bot)
if __name__ == "__main__": asyncio.run(main())