import logging

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import (
    BOT_TOKEN,
    ADMIN_NAME,
    ADMIN_PHONE,
    CHANNEL_USERNAME
)

from keyboards import (
    main_menu,
    join_channel_keyboard
)

from database import (
    init_db
)

from order import (
    order_handler
)

from ai import ask_ai


logging.basicConfig(

    format="%(asctime)s | %(levelname)s | %(message)s",

    level=logging.INFO

)


async def start(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    text = f"""
سلام 👋

به ربات رسمی

{ADMIN_NAME}

خوش آمدید.

🏗 فروش عمده و خرده سیمان

📍 اصفهان

حداقل سفارش:
۵ تن

از منوی زیر استفاده کنید.
"""

    await update.message.reply_text(

        text,

        reply_markup=main_menu()

    )


async def price(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    await update.message.reply_text(

        """
💰 قیمت روز سیمان

برای دریافت قیمت لحظه‌ای

☎️ 09130127941

تماس بگیرید.
"""

    )


async def delivery(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    await update.message.reply_text(

        """
🚚 هزینه حمل

بر اساس

✅ شهر مقصد

✅ مقدار بار

✅ نوع خودرو

محاسبه می‌شود.
"""

    )


async def contact(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    await update.message.reply_text(

        f"""
☎️ {ADMIN_NAME}

📞 {ADMIN_PHONE}

📢 {CHANNEL_USERNAME}
"""

    )


async def channel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    await update.message.reply_text(

        "برای عضویت روی دکمه زیر بزنید.",

        reply_markup=join_channel_keyboard()

    )
    async def ai_chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    menu_buttons = [
        "💰 قیمت روز سیمان",
        "📦 ثبت سفارش",
        "🚚 هزینه حمل",
        "📢 کانال تلگرام",
        "☎️ تماس با ما"
    ]

    if text in menu_buttons:
        return

    try:

        answer = await ask_ai(text)

        await update.message.reply_text(answer)

    except Exception as e:

        logging.error(e)

        await update.message.reply_text(

            "در حال حاضر ارتباط با هوش مصنوعی برقرار نیست."

        )


async def callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "check_join":

        await query.edit_message_text(

            "✅ عضویت شما تایید شد."

        )


def create_app():

    app = Application.builder().token(

        BOT_TOKEN

    ).build()

    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )

    app.add_handler(

        CallbackQueryHandler(

            callback

        )

    )

    app.add_handler(

        order_handler()

    )

    app.add_handler(

        MessageHandler(

            filters.Regex("^💰 قیمت روز سیمان$"),

            price

        )

    )

    app.add_handler(

        MessageHandler(

            filters.Regex("^🚚 هزینه حمل$"),

            delivery

        )

    )

    app.add_handler(

        MessageHandler(

            filters.Regex("^☎️ تماس با ما$"),

            contact

        )

    )

    app.add_handler(

        MessageHandler(

            filters.Regex("^📢 کانال تلگرام$"),

            channel

        )

    )

    app.add_handler(

        MessageHandler(

            filters.TEXT &

            ~filters.COMMAND,

            ai_chat

        )

    )

    return app
    def main():

    import asyncio

    asyncio.run(

        init_db()

    )

    app = create_app()

    logging.info(

        "Ghoghnoos Cement Bot Started..."

    )

    app.run_polling(

        allowed_updates=Update.ALL_TYPES

    )


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logging.info(

            "Bot Stopped."

        )

    except Exception as e:

        logging.exception(e)
