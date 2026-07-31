from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)

from database import add_order
from keyboards import main_menu

NAME = 1
PHONE = 2
CITY = 3
AMOUNT = 4
DESCRIPTION = 5


async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "📦 ثبت سفارش سیمان\n\n"
        "لطفاً نام و نام خانوادگی خود را وارد کنید."

    )

    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(

        "📱 شماره تماس خود را وارد کنید."

    )

    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(

        "📍 شهر مقصد را وارد کنید."

    )

    return CITY


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["city"] = update.message.text

    await update.message.reply_text(

        "🚚 مقدار سیمان مورد نیاز (بر حسب تن) را وارد کنید."

    )

    return AMOUNT


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["amount"] = update.message.text

    await update.message.reply_text(

        "📝 اگر توضیحی دارید بنویسید.\n"
        "در غیر این صورت بنویسید:\n"
        "ندارد"

    )
  async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["description"] = update.message.text

    await add_order(

        context.user_data["name"],

        context.user_data["phone"],

        context.user_data["city"],

        context.user_data["amount"],

        context.user_data["description"]

    )

    message = f"""
✅ سفارش شما با موفقیت ثبت شد.

👤 نام:
{context.user_data["name"]}

📱 تلفن:
{context.user_data["phone"]}

📍 شهر:
{context.user_data["city"]}

🚚 مقدار:
{context.user_data["amount"]} تن

📝 توضیحات:
{context.user_data["description"]}

کارشناس فروش در اولین فرصت با شما تماس خواهد گرفت.

☎️ 09130127941
"""

    await update.message.reply_text(

        message,

        reply_markup=main_menu()

    )

    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(

        "❌ ثبت سفارش لغو شد.",

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

                    get_name

                )

            ],

            PHONE: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    get_phone

                )

            ],

            CITY: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    get_city

                )

            ],

            AMOUNT: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    get_amount

                )

            ],

            DESCRIPTION: [

                MessageHandler(

                    filters.TEXT & ~filters.COMMAND,

                    get_description

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

    return DESCRIPTION
