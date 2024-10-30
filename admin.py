from aiogram import types

# Admin ID (admin ID ni sizning ID raqamingizga almashtiring)
ADMIN_ID = 971753760


async def admin_panel(message: types.Message, db):
    if message.from_user.id == ADMIN_ID:
        await message.reply("Mahsulot qo'shish uchun: /add_product <nom> <narx>")
    else:
        await message.reply("Kechirasiz, siz admin emassiz.")


async def add_product(message: types.Message, db):
    try:
        command_parts = message.text.split(maxsplit=2)
        if len(command_parts) < 3:
            await message.reply("Mahsulot nomi va narxini to'liq kiriting: /add_product <nom> <narx>")
            return

        name = command_parts[1]
        price = float(command_parts[2])

        # Mahsulot qo'shilishi
        success = db.add_product(name, price)  # Bu yerda qo'shilayotgan mahsulot natijasini qaytarish
        if success:  # Agar qo'shilsa, True qaytarsa
            await message.reply("Mahsulot muvaffaqiyatli qo'shildi.")
        else:
            await message.reply("Mahsulot qo'shishda xatolik yuz berdi.")

    except ValueError:
        await message.reply("Mahsulot narxini to'g'ri formatda kiriting. Masalan: /add_product Kitob 30000")
    except Exception as e:
        await message.reply(f"Mahsulot qo'shishda xatolik yuz berdi: {str(e)}")
