from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

from config import ADMIN_PHONE

from database import (
    get_orders,
    count_orders,
    delete_order,
)


def is_admin(update: Update):

    if update.effective_user is None:
        return False

    return (
        update.effective_user.username
        and update.effective_user.username.lower()
        == "hamzehb60"
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):

        await update.message.reply_text(
            "⛔ شما مدیر نیستید."
        )

        return

    total = await count_orders()

    text = f"""
👨‍💼 پنل مدیریت

📦 تعداد سفارش‌ها:
{total}

دستورات:

/orders
/stats
/delete
"""

    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    total = await count_orders()

    await update.message.reply_text(

        f"📊 تعداد کل سفارش‌ها: {total}"

    )
  async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    orders_list = await get_orders()

    if not orders_list:

        await update.message.reply_text(
            "📭 هنوز سفارشی ثبت نشده است."
        )

        return

    for order in orders_list:

        order_id = order[0]
        name = order[1]
        phone = order[2]
        city = order[3]
        amount = order[4]
        description = order[5]
        created = order[6]

        text = f"""
🆔 سفارش #{order_id}

👤 نام:
{name}

📞 تلفن:
{phone}

📍 شهر:
{city}

🏗 مقدار:
{amount}

📝 توضیحات:
{description}

🕒 تاریخ:
{created}
"""

        await update.message.reply_text(text)


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    if len(context.args) == 0:

        await update.message.reply_text(

            "نمونه:\n/delete 5"

        )

        return

    try:

        order_id = int(context.args[0])

    except ValueError:

        await update.message.reply_text(

            "شناسه سفارش صحیح نیست."

        )

        return

    await delete_order(order_id)

    await update.message.reply_text(

        f"✅ سفارش {order_id} حذف شد."
    )


def admin_handlers():

    return [

        CommandHandler(
            "admin",
            admin,
        ),

        CommandHandler(
            "orders",
            orders,
        ),

        CommandHandler(
            "stats",
            stats,
        ),

        CommandHandler(
            "delete",
            delete,
        ),

    ]
  def register_admin_handlers(application):

    for handler in admin_handlers():

        application.add_handler(handler)
