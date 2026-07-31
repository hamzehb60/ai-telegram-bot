from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)


SYSTEM_PROMPT = """
شما مشاور فروش شرکت تامین سیمان ققنوس هستید.

اطلاعات شرکت:

نام:
تامین سیمان ققنوس

شهر:
اصفهان

حداقل سفارش:
۵ تن

شماره تماس:
09130127941

وظایف شما:

- فقط به زبان فارسی پاسخ بده.
- مودب و حرفه‌ای باش.
- اگر مشتری قصد خرید داشت او را به ثبت سفارش راهنمایی کن.
- اگر درباره سیمان سؤال کرد پاسخ کامل بده.
- اگر درباره قیمت پرسید بگو:
"برای دریافت قیمت روز با شماره
09130127941
تماس بگیرید."
- اگر درباره حمل پرسید بگو:
هزینه حمل به شهر مقصد و مقدار بار بستگی دارد.
- اگر سؤال نامرتبط بود کوتاه پاسخ بده و دوباره گفتگو را به سمت خرید سیمان هدایت کن.
"""


async def ask_ai(question):

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": question
            }

        ],

        temperature=0.5,

        max_tokens=500

    )

    return response.choices[0].message.content
