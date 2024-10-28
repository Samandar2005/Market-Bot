from aiogram import types


async def process_payment(message: types.Message):
    await message.reply("To'lov amalga oshirilmoqda. Mahalliy to'lov tizimiga yo'naltirilasiz.")
    # To'lov tizimi API'ga yo'naltiruvchi kod
