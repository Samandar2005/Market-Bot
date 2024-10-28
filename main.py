import logging
from aiogram import Bot, Dispatcher, types
import asyncio

from db import Database
from products import show_products, add_to_cart
from admin import admin_panel
from payment import process_payment

API_TOKEN = '8026381986:AAHIMcczzthKYFl33TycsgLQY-e3iZ0tStA'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = Database()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Salom! Men online do'kon botiman. Mahsulotlarni ko'rish uchun /products ni kiriting yoki savatni tekshirish uchun /cart ni kiriting.")


@dp.message_handler(commands=['products'])
async def products(message: types.Message):
    await show_products(message, db)


@dp.message_handler(commands=['add_to_cart'])
async def add_to_cart_handler(message: types.Message):
    await add_to_cart(message, db)


@dp.message_handler(commands=['cart'])
async def view_cart(message: types.Message):
    await db.view_cart(message)


@dp.message_handler(commands=['pay'])
async def pay(message: types.Message):
    await process_payment(message)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    await admin_panel(message, db)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

