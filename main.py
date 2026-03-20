import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

from config import BOT_TOKEN, ADMIN_ID, CHANNEL_ID
from db import add_post, get_post, update_status, get_user_posts
from keyboards import main_menu, moderation_kb

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
    "👋 Привет!\n\n"
    "Здесь ты можешь разместить свой пост в нашем канале."
    "📌 Как это работает:"
    "1. Нажимаешь «ВЫЛОЖИТЬ ПОСТ»"
    "2. Пишешь текст"
    "3. Я отправляю его на модерацию"
    "После проверки пост появится в канале 🚀",
    reply_markup=main_menu()
)


@dp.message(F.text == "ВЫЛОЖИТЬ ПОСТ")
async def create_post(message: types.Message):
    await message.answer(
    "📋 Что должно быть в заявке:
     • 📍 Адрес
     • ⏰ Время выполнения работы
     • 👷 Количество грузчиков
     • 🧾 Описание задачи (что нужно сделать)
     • 💰 Оплата (руб./час)

     ⚠️ Важно:
Заявки без полного набора данных не рассматриваются и не публикуются."
)

@dp.message(F.text == "МОИ ПОСТЫ")
async def my_posts(message: types.Message):
    posts = get_user_posts(message.from_user.id)

    if not posts:
        await message.answer("У тебя пока нет постов")
        return

    status_map = {
        "pending": "⏳ На модерации",
        "approved": "✅ Опубликован",
        "rejected": "❌ Отклонён"
    }

    text = ""
    for p in posts:
        text += f"{p[0]}\nСтатус: {status_map.get(p[1], p[1])}\n\n"

    await message.answer(text)


@dp.message(F.text == "ПОМОЩЬ")
async def help_msg(message: types.Message):
    await message.answer("По всем вопросам: @your_username")


@dp.message()
async def handle_post(message: types.Message):
    text = message.text

    post_id = add_post(message.from_user.id, text)

    await bot.send_message(
        ADMIN_ID,
        f"Новый пост:\n\n{text}",
        reply_markup=moderation_kb(post_id)
    )

    await message.answer("Пост отправлен на модерацию!")


@dp.callback_query(F.data.startswith("approve_"))
async def approve(callback: types.CallbackQuery):
    post_id = int(callback.data.split("_")[1])

    post = get_post(post_id)
    if not post:
        return

    formatted = (
    f"📢 Новый пост\n\n"
    f"{post[0]}\n\n"
    f"👤 Автор: @{callback.from_user.username or 'не указан'}"
)

await bot.send_message(CHANNEL_ID, formatted)
    update_status(post_id, "approved")

    await callback.message.edit_text("✅ Опубликовано")


@dp.callback_query(F.data.startswith("reject_"))
async def reject(callback: types.CallbackQuery):
    post_id = int(callback.data.split("_")[1])

    # получаем пользователя
    cursor.execute("SELECT user_id FROM posts WHERE id=?", (post_id,))
    user_id = cursor.fetchone()[0]

    update_status(post_id, "rejected")

    # уведомление пользователю
    await bot.send_message(user_id, "❌ Твой пост отклонён модератором")

    await callback.message.edit_text("❌ Отклонено")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
