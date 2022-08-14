import logging.config

from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import bot
from qiwi import main, checking_payment
from database import add_bill, paid, check_block_user
from config import logger_config

logging.config.dictConfig(logger_config)

logger = logging.getLogger('main')


def is_float(element: str) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        logger.warning('Пользователь ввел не число.')
        return False


async def command_start(message: Message):
    if not check_block_user(message.from_user.id):
        ans = f'Привет, {message.from_user.username}\n\nЯ - бот для пополнения баланса. Нажмите на кнопку, чтобы пополнить баланс.'
        url_batton = InlineKeyboardButton(text='Оплатить', callback_data='ISYWFB')
        url_kb = InlineKeyboardMarkup(row_width=1)
        url_kb.add(url_batton)
        await message.answer(ans, reply_markup=url_kb)

async def cm_start(callback_query: CallbackQuery):
    if not check_block_user(callback_query.from_user.id):  
        cbd = 'Введите сумму, на которую вы хотите пополнить баланс'
        await bot.send_message(callback_query.from_user.id, cbd)

async def load_summa(message: Message):
    if not check_block_user(message.from_user.id):
        if is_float(message.text):
            bill = await main(abs(float(message.text)))
            bill_id = bill[0]
            bill_url = bill[1]

        add_bill(message.from_user.id, bill_id, float(message.text))

        ans = 'Счет успешно создан.'
        url_batton1 = InlineKeyboardButton(text='Счет', url=bill_url)
        url_batton2 = InlineKeyboardButton(text='Проверка', callback_data='AWCHPY'+bill_id)
        url_kb = InlineKeyboardMarkup(row_width=2)
        url_kb.add(url_batton1, url_batton2)
        await message.answer(ans, reply_markup=url_kb)
    

async def callback_checking(callback_query: CallbackQuery):
    print(callback_query.from_user.id)
    bill_id = callback_query.data[6::]
    print(bill_id)
    if checking_payment(bill_id) == 'PAID':
        paid(bill_id)
        await bot.send_message(callback_query.from_user.id, 'Счет оплачен, ваш баланс пополнен.')
        logger.info(f'Пользователь {callback_query.from_user.id} оплатил счет {bill_id}')
    else:
        await bot.send_message(callback_query.from_user.id, 'Счет не оплачен.')

    
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_callback_query_handler(cm_start, text='ISYWFB')
    dp.register_callback_query_handler(callback_checking, text_contains='AWCHPY')
    dp.register_message_handler(load_summa)