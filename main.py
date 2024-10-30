import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
import asyncio

from db import Database
from products import show_products, add_to_cart
from admin import admin_panel, add_product  # add_product funktsiyasini import qilamiz
from payment import process_payment

API_TOKEN = '8026381986:AAHIMcczzthKYFl33TycsgLQY-e3iZ0tStA'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)

db = Database()

# 2 ustunli asosiy menyu tugmalari
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Products'), KeyboardButton(text='Cart')],
        [KeyboardButton(text='Pay'), KeyboardButton(text='Admin')]
    ],
    resize_keyboard=True
)

@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    welcome_text = (
        "Salom! Men online do'kon botiman. Bu yerda siz mahsulotlarni ko'rishingiz, "
        "savatga qo'shishingiz va to'lovni amalga oshirishingiz mumkin.\n\n"
        "Mavjud buyruqlar:\n"
        "- Products - Mahsulotlarni ko'rish\n"
        "- Cart - Savatni ko'rish\n"
        "- Pay - To'lovni amalga oshirish\n"
        "- Admin - Administrator paneliga kirish"
    )
    await message.reply(welcome_text, reply_markup=menu_keyboard)

@router.message(lambda message: message.text == 'Products')
async def products(message: types.Message):
    await show_products(message, db)

@router.message(lambda message: message.text == 'Cart')
async def view_cart(message: types.Message):
    await db.view_cart(message)

@router.message(lambda message: message.text == 'Pay')
async def pay(message: types.Message):
    await process_payment(message)

@router.message(lambda message: message.text == 'Admin')
async def admin(message: types.Message):
    await admin_panel(message, db)

@router.message(Command(commands=['add_product']))
async def add_product_handler(message: types.Message):
    await add_product(message, db)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
