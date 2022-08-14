from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Кнопки клавиатуры админа
button_get_users = KeyboardButton(text="/Пользователи_и_их_баланс")
button_get_logs = KeyboardButton("/Логи")
button_change_balance = KeyboardButton(text="/Изменить_баланс")
button_block_user = KeyboardButton("/Блокирование_пользователя")

button_case_admin = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(button_get_users)
    .add(button_get_logs)
    .add(button_change_balance)
    .add(button_block_user)
)