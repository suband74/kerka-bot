from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from settings import BOT_TOKEN


storage = RedisStorage2('storage', db=5, pool_size=10, prefix='my_fsm_key')

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
