import logging

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config import (
    BOT_TOKEN,
    ADMIN_NAME,
    ADMIN_PHONE,
    CHANNEL_USERNAME,
)

from keyboards import (
    main_menu,
    join_channel_keyboard,
)

from ai import ask_ai

from database import init_db

from order import order_handler


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = f"""
👋 سلام

به ربات رسمی

🏢 {ADMIN_NAME}

خوش آمدید.

📍 اصفهان

🏗 فروش عمده و خرده سیمان

حداقل سفارش:
۵ تن

از منوی زیر استفاده کنید.
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu(),
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"""
💰 قیمت روز سیمان

برای دریافت قیمت لحظه‌ای

☎️ {ADMIN_PHONE}

تماس بگیرید.
"""
    )


async def delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
🚚 هزینه حمل

هزینه حمل به

✅ شهر مقصد

✅ مقدار بار

✅ نوع خودرو

بستگی دارد.
"""
    )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"""
☎️ تماس با ما

👤 {ADMIN_NAME}

📱 {ADMIN_PHONE}

📢 {CHANNEL_USERNAME}
"""
    )


async def channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "برای عضویت روی دکمه زیر کلیک کنید.",
        reply_markup=join_channel_keyboard(),
    )
    async def ai_chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = update.message.text.strip()

    ignore_buttons = [
        "💰 قیمت روز سیمان",
        "📦 ثبت سفارش",
        "🚚 هزینه حمل",
        "📢 کانال تلگرام",
        "☎️ تماس با ما",
        "🤖 مشاوره خرید",
    ]

    if text in ignore_buttons:
        return

    try:

        answer = await ask_ai(text)

        await update.message.reply_text(answer)

    except Exception as e:

        logger.error(e)

        await update.message.reply_text(
            "❌ ارتباط با هوش مصنوعی برقرار نشد."
        )


async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    if query.data == "check_join":

        try:

            member = await context.bot.get_chat_member(
                CHANNEL_USERNAME,
                query.from_user.id,
            )

            if member.status in [
                "member",
                "administrator",
                "creator",
            ]:

                await query.edit_message_text(
                    "✅ عضویت شما تایید شد."
                )

            else:

                await query.answer(
                    "ابتدا عضو کانال شوید.",
                    show_alert=True,
                )

        except Exception:

            await query.answer(
                "امکان بررسی عضویت وجود ندارد.",
                show_alert=True,
            )


def create_application():

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_handler
        )
    )

    application.add_handler(
        order_handler()
    )
        application.add_handler(
        MessageHandler(
            filters.Regex("^💰 قیمت روز سیمان$"),
            price,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^🚚 هزینه حمل$"),
            delivery,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^☎️ تماس با ما$"),
            contact,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^📢 کانال تلگرام$"),
            channel,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^🤖 مشاوره خرید$"),
            ai_chat,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_chat,
        )
    )

    return application


def main():

    import asyncio

    asyncio.run(
        init_db()
    )

    app = create_application()

    logger.info("Ghoghnoos Cement Bot Started")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.info("Bot Stopped")

    except Exception as error:

        logger.exception(error)
        
