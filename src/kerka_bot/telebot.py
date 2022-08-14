from aiogram.utils import executor

from create_bot import dp
from handlers import client, admin


async def on_startup(dp):
    print("Бот онлайн")

async def on_shutdown(dp):
    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
