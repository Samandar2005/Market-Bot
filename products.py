from aiogram import types


async def show_products(message: types.Message, db):
    """Displays all available products to the user."""
    products = db.get_products()
    if not products:
        await message.reply("Hozircha mahsulotlar mavjud emas.")
    else:
        product_list = "\n".join([f"{product[1]} - {product[2]:,.0f} so'm" for product in products])
        await message.reply(f"Mavjud mahsulotlar:\n{product_list}")


async def add_to_cart(message: types.Message, db):
    """
    Adds a product to the user's cart.
    Usage example: "/add_to_cart <product_id> <quantity>"
    """
    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            await message.reply("Formatni to'g'ri kiriting: /add_to_cart <product_id> <quantity>")
            return

        # Extract product_id and quantity from message
        product_id = int(command_parts[1])
        quantity = int(command_parts[2])

        # Check if the product exists in the database
        products = db.get_products()
        product_ids = [product[0] for product in products]

        if product_id not in product_ids:
            await message.reply("Bunday mahsulot mavjud emas.")
            return

        # Add to cart if the product is valid
        db.add_to_cart(message.from_user.id, product_id, quantity)
        await message.reply("Mahsulot savatga qo'shildi.")
    except ValueError:
        await message.reply("Mahsulot ID va miqdorni to'g'ri formatda kiriting: butun sonlar kiritilishi kerak.")
    except Exception as e:
        await message.reply(f"Mahsulotni qo'shishda xatolik yuz berdi: {str(e)}")
