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

@dp.message(F.text == "📦 Склад")
async def show_instractions(message:Message):
    await message.answer("""
📦 Warehouse Products

📝 Command Format:
/products warehouse_name

💡 Example:
/products MainWarehouse ✨

🚀 Use the command above to view all products in your warehouse.

""")

@dp.message(Command("products"))
async def show_all(message: Message , command:CommandObject):
    sklad_name = command.args
    if sklad_name is None:
        await message.answer("""
⚠️ Warehouse name is missing!

Please enter the command in this format:

📦 /products warehouse_name

💡 Example:
/products MainWarehouse

✨ Please provide a warehouse name after the command.
""")
    else:
        show = await products(message.from_user.id , sklad_name)
        if show is None:
            await message.answer("""
📦 Your Warehouse Has No Products Yet!

⚠️ There are currently no products in this warehouse.

➕ Add a product to your warehouse to start managing your stock!
""")
        else:
            text = "📦 Your Products:\n"
            for i in show:
                text += f"""
🏷️ Product Name: {i['product_name']}
🔢 Quantity: {i['quantity']}

📊 Stock information displayed successfully!
            """
            await message.answer(f"{text}")

@dp.message(Command("restock"))
async def add_to_product(message:Message , command:CommandObject):
    add_to_prd = command.args
    if add_to_prd is None:
        await message.answer("""
⚠️ Invalid or missing information!

Please enter the command in this format:

📦 /restock product_name/adding_quantity/sklad_id

💡 Example:
/restock Coca-Cola/50/1

✅ Make sure all three values are entered correctly.


""")        
    else:
        add_to_prd = add_to_prd.split("/")
        await restock(add_to_prd[0] , add_to_prd[1] , message.from_user.id , add_to_prd[2])
        await message.answer(f"""
✅ Quantity Updated Successfully!

📦 Product: {add_to_prd[0]}
🔢 The quantity has been updated successfully.
""")

@dp.message(Command("sell"))
async def add_to_product(message:Message , command:CommandObject):
    remove_from_prd = command.args
    if remove_from_prd is None:
        await message.answer("""
⚠️ Invalid or missing information!

Please enter the command in this format:

📤 /sell product_name/removing_quantity/sklad_id

💡 Example:
/sell Coca-Cola/10/1

✅ Make sure all three values are entered correctly.


""")        
    else:
        remove_from_prd = remove_from_prd.split("/")
        await sell(remove_from_prd[0] , remove_from_prd[1] , message.from_user.id , remove_from_prd[2])
        await message.answer(f"""
✅ Quantity Updated Successfully!

📦 Product: {remove_from_prd[0]}

📊 Your warehouse stock has been updated.

""")

@dp.message(F.text == "⚠️ Заканчивается")
async def info_about_lf_func(message: Message):
    await message.answer("""
📉 Low Stock

To check products with low stock, use the command:

👉 /low_stock warehouse_name

💡 Example:
/low_stock MainWarehouse

📦 Enter the name of the warehouse you want to check.
""")


@dp.message(Command("low_stock"))
async def low_stk(message:Message , command:CommandObject):
    get_sklad_name = command.args

    if get_sklad_name is None:
        await message.answer("""
⚠️ Invalid or missing information!

Please enter the command in this format:

📉 /low_stock warehouse_name

💡 Example:
/low_stock MainWarehouse

✅ Make sure to enter the warehouse name after the command.


""")
    else:
        show_low_stock = await low_stock(message.from_user.id , get_sklad_name)
        if len(show_low_stock) <= 0:
            await message.answer("""
📦 No Low-Stock Products

✅ You don't have any products with a quantity below their low-stock threshold.

📊 Your stock levels are currently sufficient!

""")
        else:
            text = "⚠️ Low-Stock Products:\n"
            for i in show_low_stock:
                text += f"""
📦 Product ID: {i['product_id']}
🏷️ Product Name: {i['product_name']}
🔢 Quantity: {i['quantity']}
👤 Warehouse Owner Telegram ID: {i['tg_id']}
🏢 Warehouse Name: {i['name']}\n
            """    
            text += "🚨 This product is below the low-stock threshold.\n"
            await message.answer(f"{text}")

@dp.message(Command("help"))
async def help(message:Message):
    await message.answer("""
🤖 Warehouse Stock Manager — Help

📦 Manage your warehouses and keep track of your inventory with ease!

━━━━━━━━━━━━━━━━━━

🚀 Basic Commands

🔹 /start — Start the bot and open the main menu.

🏢 /create_sklad — Create a new warehouse and add its name.

📋 /see_sklads — View all your warehouses.

➕ /add_product — Add a new product to a warehouse. Enter: product name / quantity / low-stock threshold / warehouse ID.

📦 /products — View all products in a selected warehouse.

🔄 /restock — Increase a product's quantity. Enter: product name / adding quantity / warehouse ID.

📤 /sell — Decrease a product's quantity. Enter: product name / removing quantity / warehouse ID.

⚠️ /low_stock — View products whose quantity is below their low-stock threshold. Enter: warehouse name.

❓ /help — Show this help menu.

━━━━━━━━━━━━━━━━━━

📊 Keep your stock organized. Keep your business moving! 🚀
""")

@dp.message()
async def wrong_message(message: Message):
    await message.answer("""
⚠️ Unknown Command

I don't recognize that command or message. 🤔

📋 Please use one of the available commands below:

❓ /help — View all available commands
🚀 /start — Start the bot

💡 Tip: Make sure you enter a valid command beginning with /.

""")

async def main():
    print("Bot started")
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())