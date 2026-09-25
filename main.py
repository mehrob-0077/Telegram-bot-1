import asyncio
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from connection import create_table
from service import *
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token)
dp = Dispatcher()


@dp.message(Command("start"))
async def startbot(message: Message):
    user = await get_user(message.from_user.id)

    if user:
        await message.answer(
            f"Hello {message.from_user.first_name} dear!"
        )
    else:
        await save_user(message.from_user.id,message.from_user.username,message.from_user.first_name,message.from_user.last_name
        )
        await message.answer(
            f"Hello {message.from_user.first_name} dear!"
        )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("""
Menu helps
Команды:
/start - for start bot
/show_users - for show all users
/add_task - for add task
/show_task - for show all tasks
""")


@dp.message(Command("add_task"))
async def add_task(message: Message, command: CommandObject):
    task = command.args

    if not task:
        await message.answer("Enter your task.")
        return

    sav = await save_task(message.from_user.id, task)

    if sav:
        await message.answer("Task saved successfully!")
    else:
        await message.answer("Error saving task.")


@dp.message(Command("show_users"))
async def show_users_command(message: Message):
    users = await show_users()

    text = "Users:\n"

    for i in users:
        text += f"{i['full_name']}\n"

    await message.answer(text)

@dp.message(Command("show_task"))
async def show_task_command(message: Message):
    tasks = await show_tasks(message.from_user.id)

    if not tasks:
        await message.answer("You don't have any tasks yet.")
        return

    text = "Your Tasks:\n"

    for i in tasks:
        text += f"{i['task_text']}\n"
    
    await message.answer(text)

async def main():
    print("Start Bot")
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())