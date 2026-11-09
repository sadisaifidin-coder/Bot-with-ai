import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from ai_chat import chat, generate_image, search


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_modes: dict[int, str] = {}

def get_main_keybord():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="ИИ ЧАТ"))
    builder.add(types.KeyboardButton(text="🎨 ТАҲИЯИ РАСМ"))
    builder.add(types.KeyboardButton(text="🔍 ҶУСТУҶӮ"))
    builder.add(types.KeyboardButton(text="👋 Салом"))
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Тугмаи поёнро барои оғози сӯҳбат бо ИИ пахш кунед.', reply_markup=get_main_keybord())

@dp.message(lambda message: message.text == "ИИ ЧАТ")
async def say_hello(message: types.Message):
    user_modes[message.from_user.id] = "chat"
    await message.answer('Режими сӯҳбат бо ИИ оғоз шуд. Лутфан саволи худро нависед.')

@dp.message(lambda message: message.text == "🎨 ТАҲИЯИ РАСМ")
async def create_image(message: types.Message):
    user_modes[message.from_user.id] = "image"
    await message.answer('Чи гуна расм таҳия кардан лозим? Промти худро нависед.')

@dp.message(lambda message: message.text == "🔍 ҶУСТУҶӮ")
async def search_in_web(message: types.Message):
    user_modes[message.from_user.id] = "search"
    await message.answer('Чиро ҷустуҷӯ кардан мехоҳед? Саволи худро нависед.')

@dp.message(lambda message: message.text == "👋 Салом")
async def greet_user(message: types.Message):
    await message.answer('Салом!.')


@dp.message()
async def ai_response(message: types.Message):

    if (user_modes[message.from_user.id] == "chat"):
        await message.answer('Фикр карда истодаам...')
        anwer = chat(message.from_user.id, message.text)
        await message.answer(anwer)

    elif (user_modes[message.from_user.id] == "image"):
        await message.answer('🎨Расми шуморо таҳия карда истодаам...')
        try:
            filename = generate_image(message.from_user.id, message.text)
            photo = FSInputFile(filename)
            await message.answer_photo(photo, caption="Марҳамат, расми таҳиякардаи шумо!")
        except Exception as e:
            await message.answer(f"Хато рӯй дод: {str(e)}")

    elif (user_modes[message.from_user.id] == "search"):
        await message.answer('🔍Дар ҷустуҷӯ...')
        result = search(message.text)
        await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
