import asyncio
from dotenv import load_dotenv
from aiogram import Dispatcher , Bot , F
from aiogram.types import Message , ReplyKeyboardMarkup , KeyboardButton
from aiogram.filters import CommandStart , Command , CommandObject
from connection import create_table
from service import *
import os

load_dotenv()

token = os.getenv("token")
bot = Bot(token)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📦 Склад"),
            KeyboardButton(text="⚠️ Заканчивается")
        ]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def greet(message: Message):
    await message.answer(f"""
👋 Welcome to Warehouse Stock Manager! 📦

🏢 Your smart assistant for simple and efficient warehouse management.

✨ What you can do:

📦 ➜ Manage your inventory
➕ ➜ Add new products
🔍 ➜ View your products
📊 ➜ Check stock levels
🔄 ➜ Restock or sell products
⚠️ ➜ Monitor low-stock products
💬 ➜ View all commands with /help

━━━━━━━━━━━━━━━━━━

⚡ Fast. Simple. Organized.

🚀 Keep your inventory under control and your warehouse running smoothly!

👇 Choose an action from the menu below or type a command to get started.
""" , reply_markup=main_kb)

@dp.message(Command("create_sklad"))
async def create_skl(message:Message , command:Command):
    sklad_name = command.args
    if sklad_name is None:
        await message.answer("""
⚠️ Warehouse name is missing!

Please enter the warehouse name using this format:

📦 /create_sklad warehouse_name

💡 Example:
/create_sklad Main Warehouse

✅ Make sure to provide the warehouse name after the command.
""")
    else:
        await create_sklad(message.from_user.full_name , message.from_user.id , sklad_name)
        await message.answer("""
🎉 Warehouse Created Successfully!

📦 Your warehouse has been created and is ready to use.
✅ You can now start adding products and managing your stock.
""")

@dp.message(Command("see_sklads"))
async def see_skl(message:Message):
    show_skl = await see_my_sklads(message.from_user.id)
    if show_skl is None:
        await message.answer("""
⚠️ You don't have any warehouses yet!

📦 You can create one using the command:

👉 /create_sklad warehouse_name

💡 Example:
/create_sklad Main Warehouse

🚀 Create your first warehouse and start managing your stock!
""")
    else:
        text = "📦 Your Warehouses:\n"
        for i in show_skl:
            text += f"""
🏷️ Warehouse ID: {i['sklad_id']}
📛 Warehouse Name: {i['name']}
👤 Creator: {i['creator']}
📅 Created At: {i['created_at']}
🆔 Telegram ID: {i['tg_id']}\n
        """  
        await message.answer(f"{text}")


@dp.message(Command("add_product"))
async def add(message:Message , command:CommandObject):
    product = command.args
    if product is None:
        await message.answer("""
⚠️ Invalid format!

Please enter the product information in this format after /add_product:

📦 Product Name/Quantity/Low Stock Threshold/Sklad id

📝 Example:
Apples/50/10

✅ Please make sure all 3 values are entered correctly.
    """)
    else:
        product = product.split("/")
        product[1] = int(product[1])
        product[2] = int(product[2])
        await add_product(product[0] , product[1] , product[2] , message.from_user.id , product[3])
        await message.answer(f"""
📦 Product Added Successfully!

✅ {product[0]} has been added to your warehouse.

📊 Your stock has been updated successfully!
""")

