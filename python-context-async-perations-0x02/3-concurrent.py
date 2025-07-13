import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def fetch_concurrently():
    # Run both queries at once
    users, older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print('All users:', users)
    print('Users > 40:', older)

if __name__ == '__main__':
    asyncio.run(fetch_concurrently())
