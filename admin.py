from aiogram import types


async def admin_panel(message: types.Message, db):
    if message.from_user.id == 971753760:  # Admin ID ni kiriting
        await message.reply("Mahsulot qo'shish uchun: /add_product <nom> <narx>")
    else:
        await message.reply("Kechirasiz, siz admin emassiz.")


async def add_product(message: types.Message, db):
    try:
        _, name, price = message.text.split()
        db.add_product(name, float(price))
        await message.reply("Mahsulot muvaffaqiyatli qo'shildi.")
    except Exception as e:
        await message.reply("Mahsulot qo'shishda xatolik yuz berdi.")
