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
        "Привет!\n\nТы можешь отправить пост на публикацию.",
        reply_markup=main_menu()
    )


@dp.message(F.text == "ВЫЛОЖИТЬ ПОСТ")
async def create_post(message: types.Message):
    await message.answer("Напиши текст поста одним сообщением:")


@dp.message(F.text == "МОИ ПОСТЫ")
async def my_posts(message: types.Message):
    posts = get_user_posts(message.from_user.id)

    if not posts:
        await message.answer("У тебя пока нет постов")
        return

    text = ""
    for p in posts:
        text += f"{p[0]}\nСтатус: {p[1]}\n\n"

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

    await bot.send_message(CHANNEL_ID, post[0])
    update_status(post_id, "approved")

    await callback.message.edit_text("✅ Опубликовано")


@dp.callback_query(F.data.startswith("reject_"))
async def reject(callback: types.CallbackQuery):
    post_id = int(callback.data.split("_")[1])

    update_status(post_id, "rejected")
    await callback.message.edit_text("❌ Отклонено")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())