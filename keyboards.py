from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import CHANNEL_USERNAME


def main_menu():

    keyboard = [

        [
            KeyboardButton("💰 قیمت روز سیمان"),
            KeyboardButton("📦 ثبت سفارش")
        ],

        [
            KeyboardButton("🚚 هزینه حمل"),
            KeyboardButton("🤖 مشاوره خرید")
        ],

        [
            KeyboardButton("📢 کانال تلگرام"),
            KeyboardButton("☎️ تماس با ما")
        ]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )


def join_channel_keyboard():

    keyboard = [

        [

            InlineKeyboardButton(

                "📢 عضویت در کانال",

                url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"

            )

        ],

        [

            InlineKeyboardButton(

                "✅ عضو شدم",

                callback_data="check_join"

            )

        ]

    ]

    return InlineKeyboardMarkup(keyboard)
