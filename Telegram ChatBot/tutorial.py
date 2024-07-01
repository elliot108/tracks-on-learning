import asyncio
import telegram


async def main():
    bot = telegram.Bot("7431977160:AAG7mgVuOeHfhKBuSn_OPJozEAUHf5Ad6dM")
    async with bot:
        await bot.send_message(text="Lee lar", chat_id=5329305505, disable_notification=0)


if __name__ == '__main__':
    asyncio.run(main())