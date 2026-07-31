from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters,
)

from database import add_order
from keyboards import main_menu

NAME, PHONE, CITY, AMOUNT, DESCRIPTION = range(5)


async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "📦 ثبت سفارش سیمان\n\n"
        "لطفاً نام و نام خانوادگی خود را وارد کنید."
    )

    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text.strip()

    await update.message.reply_text(
        "📱 شماره تماس خود را وارد کنید."
    )

    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text.strip()

    await update.message.reply_text(
        "📍 شهر مقصد را وارد کنید."
    )

    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["city"] = update.message.text.strip()

    await update.message.reply_text(
        "🚚 مقدار سیمان (تن) را وارد کنید."
    )

    return AMOUNT


async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["amount"] = update.message.text.strip()

    await update.message.reply_text(
        "📝 اگر توضیحی دارید بنویسید.\n"
        "اگر ندارید بنویسید: ندارد"
    )

    return DESCRIPTION
    async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["description"] = update.message.text.strip()

    await add_order(

        context.user_data["name"],
        context.user_data["phone"],
        context.user_data["city"],
        context.user_data["amount"],
        context.user_data["description"]

    )

    text = f"""
✅ سفارش شما با موفقیت ثبت شد.

👤 نام:
{context.user_data["name"]}

📱 شماره تماس:
{context.user_data["phone"]}

📍 شهر مقصد:
{context.user_data["city"]}

🚚 مقدار:
{context.user_data["amount"]} تن

📝 توضیحات:
{context.user_data["description"]}

☎️ کارشناس فروش تامین سیمان ققنوس
در اولین فرصت با شما تماس خواهد گرفت.

شماره تماس:
09130127941
"""

    await update.message.reply_text(

        text,

        reply_markup=main_menu()

    )

    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(

        "ثبت سفارش لغو شد.",

        reply_markup=main_menu()

    )

    return ConversationHandler.END


def order_handler():

    return ConversationHandler(

        entry_points=[

            MessageHandler(

                filters.Regex("^📦 ثبت سفارش$"),

                start_order

            )

        ],

        states={

            NAME: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    name

                )

            ],

            PHONE: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    phone

                )

            ],

            CITY: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    city

                )

            ],

            AMOUNT: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    amount

                )

            ],

            DESCRIPTION: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    description

                )

            ]

        },

        fallbacks=[

            CommandHandler(

                "cancel",

                cancel

            )

        ]

    )
