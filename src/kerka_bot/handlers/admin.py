import logging.config
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from create_bot import bot
from keyboards.admin_kb import button_case_admin
from settings import ID
from database import user_with_balance, admin_change_balance, add_to_db_block_user
from config import logger_config


logging.config.dictConfig(logger_config)

logger = logging.getLogger('main.admin')



class FSMadmin(StatesGroup):
    user_id = State()
    amount = State()

async def fsm_start(message: Message):
    str_id = str(message.from_user.id)
    if str_id == ID:
        await FSMadmin.user_id.set()
        await message.reply("Введите ID пользователя")

async def fsm_user_id(message: Message, state: FSMContext):
    str_id = str(message.from_user.id)
    if str_id == ID:
        async with state.proxy() as data:
            data["user_id"] = int(message.text)
            await FSMadmin.next()
            await message.reply("Введите сумму исправления")

async def fsm_amount(message: Message, state: FSMContext):
    str_id = str(message.from_user.id)
    if str_id == ID:
        async with state.proxy() as data:
            data["amount"] = float(message.text)

        admin_change_balance(data["user_id"], data["amount"])
        await bot.send_message(message.from_user.id, 'Баланс пользователя успешно изменен')
        
        logger.info(f'Админ изменил баланс пользователя {data["user_id"]} на сумму {data["amount"]}')
        
        await state.finish()

async def admin_command(message: Message):
    str_id = str(message.from_user.id)
    if str_id == ID:
        await bot.send_message(
            message.from_user.id, "Выберите действие", reply_markup=button_case_admin
        )
        await message.delete()


async def cancel_handler(message: Message, state: FSMContext):
    str_id = str(message.from_user.id)
    if str_id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("Операция отменена")


async def user_balance(message: Message):
    str_id = str(message.from_user.id)
    if str_id == ID:
        sp = user_with_balance()
        await bot.send_message(message.from_user.id, f'Список пользователей{sp}.')


class FSMadminBlock(StatesGroup):
    user_id = State()


async def fsm_start_block(message: Message):
    str_id = str(message.from_user.id)
    if str_id == ID:
        await FSMadminBlock.user_id.set()
        await message.reply("Введите ID пользователя")

async def fsm_block_id(message: Message, state: FSMContext):
    str_id = str(message.from_user.id)
    if str_id == ID:
        async with state.proxy() as data:
            data["user_id"] = int(message.text)

        add_to_db_block_user(data["user_id"])
        logger.info(f'Админ заблокировал пользователя {data["user_id"]}')
        await bot.send_message(message.from_user.id, 'Пользователь заблокирован')
        await state.finish()


async def user_logs(message: Message):
    str_id = str(message.from_user.id)
    if str_id == ID:
        with open('information.log') as file:
            st = file.readlines()
        await bot.send_message(message.from_user.id, st)
        


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_command, commands=["admin"])
    dp.register_message_handler(user_balance, commands=['Пользователи_и_их_баланс'])
    dp.register_message_handler(cancel_handler, commands=["Отмена"], state="*")
    dp.register_message_handler(fsm_start, commands=['Изменить_баланс'], state=None)
    dp.register_message_handler(fsm_user_id, state=FSMadmin.user_id)
    dp.register_message_handler(fsm_amount, state=FSMadmin.amount)
    dp.register_message_handler(fsm_start_block, commands=['Блокирование_пользователя'], state=None)
    dp.register_message_handler(fsm_block_id, state=FSMadminBlock.user_id)
    dp.register_message_handler(user_logs, commands=["Логи"])