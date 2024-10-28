from aiogram import types


async def search_products(message: types.Message, db):
    query = message.text.replace('/search ', '')
    products = db.get_products()
    results = [product for product in products if query.lower() in product[1].lower()]
    if not results:
        await message.reply("Hech qanday mahsulot topilmadi.")
    else:
        for product in results:
            await message.reply(f"{product[1]} - {product[2]} so'm")
