import logging

from telegram import (
    Update,
    ReplyKeyboardRemove
)

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

from ai import ask_ai

from database import (
    init_db
)

from order import (
    order_handler
)


logging.basicConfig(

    format="%(asctime)s - %(levelname)s - %(message)s",

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

🏗 فروش سیمان عمده و خرده

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

💰 قیمت سیمان

برای دریافت قیمت لحظه‌ای

با شماره زیر تماس بگیرید.

☎️ 09130127941

"""

    )


async def delivery(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    await update.message.reply_text(

        """

🚚 هزینه حمل

براساس

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

📱 {ADMIN_PHONE}

📢 {CHANNEL_USERNAME}

"""

    )


async def channel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    await update.message.reply_text(

        "برای عضویت در کانال روی دکمه زیر بزنید.",

        reply_markup=join_channel_keyboard()

    )
  async def ai_chat(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    question = update.message.text

    ignore = [

        "💰 قیمت روز سیمان",

        "📦 ثبت سفارش",

        "🚚 هزینه حمل",

        "📢 کانال تلگرام",

        "☎️ تماس با ما"

    ]

    if question in ignore:

        return

    answer = await ask_ai(question)

    await update.message.reply_text(answer)


async def button_click(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    if query.data == "check_join":

        await query.edit_message_text(

            "✅ عضویت شما بررسی شد."

        )


def main():

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

            button_click

        )

    )

    app.add_handler(

        order_handler()

    )

    app.add_handler(

        MessageHandler(

            filters.Regex(

                "^💰 قیمت روز سیمان$"

            ),

            price

        )

    )

    app.add_handler(

        MessageHandler(

            filters.Regex(

                "^🚚 هزینه حمل$"

            ),

            delivery

        )

    )

    app.add_handler(

        MessageHandler(

            filters.Regex(

                "^☎️ تماس با ما$"

            ),

            contact

        )

    )

    app.add_handler(

        MessageHandler(

            filters.Regex(

                "^📢 کانال تلگرام$"

            ),

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

    app.run_polling()


if __name__ == "__main__":

    import asyncio

    asyncio.run(

        init_db()

    )

    main()
  
