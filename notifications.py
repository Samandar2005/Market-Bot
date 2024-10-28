from aiogram import types


async def send_notification(message: types.Message, text: str):
    await message.reply(text)
