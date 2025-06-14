import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

API_TOKEN = "8189426602:AAF-TnDhzBSyeDT17Kgsv3_uw__m4elOoT0"

ADMIN_ID = 275356106  # заміни на свій Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Завантаження підписників
def load_subscribers():
    try:
        with open("subscribers.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

# Збереження підписників
def save_subscribers(subs):
    with open("subscribers.json", "w") as f:
        json.dump(list(subs), f)

subscribers = load_subscribers()

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.chat.id
    subscribers.add(user_id)
    save_subscribers(subscribers)
    await message.answer("Ви підписалися на повідомлення.")

# Розсилка від адміна
@dp.message()
async def admin_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return  # ігноруємо чужі повідомлення

    # Розсилка всім підписникам
    for user_id in subscribers:
        try:
            await message.copy_to(chat_id=user_id)
        except Exception as e:
            print(f"❌ Не вдалося надіслати {user_id}: {e}")

    await message.answer("✅ Повідомлення розіслано всім підписникам.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())