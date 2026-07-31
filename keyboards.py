from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# منوی اصلی
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
        resize_keyboard=True,
        is_persistent=True
    )


# دکمه عضویت کانال
def join_channel_keyboard():

    keyboard = [

        [

            InlineKeyboardButton(

                text="📢 عضویت در کانال",

                url="https://t.me/+c9zWKkU5OXw4ODZk"

            )

        ],

        [

            InlineKeyboardButton(

                text="✅ عضو شدم",

                callback_data="check_join"

            )

        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# پنل مدیریت
def admin_menu():

    keyboard = [

        [

            KeyboardButton("📋 لیست سفارش‌ها"),

            KeyboardButton("📊 آمار")

        ],

        [

            KeyboardButton("📣 ارسال پیام همگانی")

        ],

        [

            KeyboardButton("🏠 بازگشت")

        ]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )
