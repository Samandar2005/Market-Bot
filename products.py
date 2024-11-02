from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def show_products(message: types.Message, db):
    """Displays all available products to the user with an 'Add to Cart' button for each product."""
    products = db.get_products()
    if not products:
        await message.reply("Hozircha mahsulotlar mavjud emas.")
    else:
        for product in products:
            product_id, name, price = product
            product_text = f"{name} - {price:,.0f} so'm"

            # Create an inline keyboard with the "Add to Cart" button
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Savatga qo'shish", callback_data=f"add_to_cart:{product_id}")]
                ]
            )

            # Send the product info with the button
            await message.reply(product_text, reply_markup=keyboard)

            await message.reply(product_text, reply_markup=keyboard)


async def add_to_cart(message: types.Message, db):
    """
    Adds a specified product to the user's cart.
    Usage example: "/add_to_cart <product_id> <quantity>"
    """
    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            await message.reply("Iltimos, formatni to'g'ri kiriting: /add_to_cart <product_id> <quantity>")
            return

        # Extract product_id and quantity from message
        product_id = int(command_parts[1])
        quantity = int(command_parts[2])

        # Validate that the quantity is a positive number
        if quantity <= 0:
            await message.reply("Miqdor musbat son bo'lishi kerak.")
            return

        # Check if the product exists in the database
        products = db.get_products()
        product_ids = [product[0] for product in products]

        if product_id not in product_ids:
            await message.reply("Bunday mahsulot mavjud emas.")
            return

        # Add to cart if the product is valid
        db.add_to_cart(message.from_user.id, product_id, quantity)
        await message.reply("Mahsulot savatga muvaffaqiyatli qo'shildi.")
    except ValueError:
        await message.reply("Mahsulot ID va miqdorni to'g'ri formatda kiriting: butun sonlar kiritilishi kerak.")
    except Exception as e:
        await message.reply(f"Mahsulotni qo'shishda xatolik yuz berdi: {str(e)}")
