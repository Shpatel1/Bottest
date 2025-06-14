import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def load_subscribers():
    try:
        with open("subscribers.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_subscribers(subs):
    with open("subscribers.json", "w") as f:
        json.dump(list(subs), f)

subscribers = load_subscribers()

@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.chat.id
    subscribers.add(user_id)
    save_subscribers(subscribers)
    await message.answer("✅ Ви підписались на повідомлення!")

@dp.message()
async def admin_message(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    for user_id in subscribers:
        try:
            await message.copy_to(chat_id=user_id)
        except Exception as e:
            print(f"❌ Не вдалося надіслати користувачу {user_id}: {e}")
    await message.answer("✅ Повідомлення надіслано всім підписникам!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
