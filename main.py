import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
import asyncio
import os

from db import Database
from products import show_products, add_to_cart
from admin import admin_panel, add_product
from payment import process_payment

API_TOKEN = "8026381986:AAHIMcczzthKYFl33TycsgLQY-e3iZ0tStA"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)
db = Database()
router = Router()
dp.include_router(router)

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
        "Salom! Men online do'kon botiman.\n"
        "Buyruqlar:\n"
        "- Products - Mahsulotlarni ko'rish\n"
        "- Cart - Savatni ko'rish\n"
        "- Pay - To'lov\n"
        "- Admin - Admin paneli"
    )
    await message.reply(welcome_text, reply_markup=menu_keyboard)


@router.message(lambda message: message.text == 'Products')
async def products(message: types.Message):
    await show_products(message, db)


@router.message(lambda message: message.text == 'Cart')
async def view_cart(message: types.Message):
    cart_items = db.view_cart(message.from_user.id)
    if not cart_items:
        await message.reply("Savatda hech qanday mahsulot yo'q.")
    else:
        cart_text = "\n".join([f"{item[0]} - {item[1]} so'm x {item[2]}" for item in cart_items])
        await message.reply(cart_text)


@router.message(lambda message: message.text == 'Pay')
async def pay(message: types.Message):
    await process_payment(message)


@router.message(lambda message: message.text == 'Admin')
async def admin(message: types.Message):
    await admin_panel(message, db)




@router.callback_query(lambda call: call.data.startswith("add_to_cart"))
async def handle_add_to_cart(call: types.CallbackQuery):
    # Extract product_id from callback data
    product_id = int(call.data.split(":")[1])

    # Call the add_to_cart function with the user ID and product ID
    await add_to_cart_callback(call, product_id, db)


async def add_to_cart_callback(call: types.CallbackQuery, product_id: int, db):
    """Adds a specified product to the user's cart based on button click."""
    try:
        # Specify quantity as 1 by default
        quantity = 1

        # Add to cart
        db.add_to_cart(call.from_user.id, product_id, quantity)
        await call.answer("Mahsulot savatga muvaffaqiyatli qo'shildi.")
    except Exception as e:
        await call.answer(f"Mahsulotni qo'shishda xatolik yuz berdi: {str(e)}", show_alert=True)



async def main():
    await dp.start_polling(bot)
    db.close()


if __name__ == "__main__":
    asyncio.run(main())
