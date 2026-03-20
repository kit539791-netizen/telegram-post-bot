from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ВЫЛОЖИТЬ ПОСТ")],
            [KeyboardButton(text="МОИ ПОСТЫ"), KeyboardButton(text="ПОМОЩЬ")]
        ],
        resize_keyboard=True
    )


def moderation_kb(post_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"approve_{post_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{post_id}")
        ]
    ])