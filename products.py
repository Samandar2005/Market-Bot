from aiogram import types

async def show_products(message: types.Message, db):
    products = db.get_products()
    if not products:
        await message.reply("Hozircha mahsulotlar mavjud emas.")
    else:
        for product in products:
            product_text = f"{product[1]} - {product[2]} so'm"
            await message.reply(product_text)

async def add_to_cart(message: types.Message, db):
    # Mahsulot ID va miqdorni olish (misol uchun "/add_to_cart 1 2" deb yozing)
    try:
        _, product_id, quantity = message.text.split()
        db.add_to_cart(message.from_user.id, int(product_id), int(quantity))
        await message.reply("Mahsulot savatga qo'shildi.")
    except Exception as e:
        await message.reply("Mahsulotni qo'shishda xatolik yuz berdi. Iltimos, formatni to'g'ri kiriting.")
