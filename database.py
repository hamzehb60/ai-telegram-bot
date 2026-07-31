import aiosqlite

DB_NAME = "cement.db"


async def init_db():

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""

        CREATE TABLE IF NOT EXISTS orders(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT,

            phone TEXT,

            city TEXT,

            amount INTEGER,

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        await db.commit()



async def add_order(

    full_name,

    phone,

    city,

    amount,

    description

):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(

            """

            INSERT INTO orders(

                full_name,

                phone,

                city,

                amount,

                description

            )

            VALUES(

                ?,?,?,?,?

            )

            """,

            (

                full_name,

                phone,

                city,

                amount,

                description

            )

        )

        await db.commit()



async def get_orders():

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(

            """

            SELECT *

            FROM orders

            ORDER BY id DESC

            """

        )

        return await cursor.fetchall()



async def count_orders():

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(

            """

            SELECT COUNT(*)

            FROM orders

            """

        )

        result = await cursor.fetchone()

        return result[0]



async def delete_order(order_id):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(

            """

            DELETE FROM orders

            WHERE id=?

            """,

            (

                order_id,

            )

        )

        await db.commit()
