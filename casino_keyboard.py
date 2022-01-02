import json
from telebot import types

# Правила
markup_inline_soglashenie = types.InlineKeyboardMarkup()
item_soglashenie = types.InlineKeyboardButton(text="✅ Принять правила", callback_data="soglashenie")
markup_inline_soglashenie.row(item_soglashenie)

# Клавиатура основная
def keyboard_osnova():
    markup_osnova = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('🎰Играть🎰')
    btn2 = types.KeyboardButton('💳Пополнить💳')
    btn3 = types.KeyboardButton('💰Вывести💰')
    btn4 = types.KeyboardButton('🏝️Личный кабинет🏝️')
    markup_osnova.row(btn1, btn4)
    markup_osnova.add(btn2, btn3)
    return markup_osnova

# Клавиатура цифры
def keyboard_chifri():
    markup_chifri = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    btn5 = types.KeyboardButton('5')
    markup_chifri.add(btn1, btn2, btn3, btn4, btn5)
    return markup_chifri

# Клавиатура "Назад" при входе в казино
def keyboard_nazad():
    markup_nazad = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Закончить игру')
    markup_nazad.row(btn1)
    return markup_nazad

# "Назад" в функциях добавления админа
def nazad_admin():
    markup_nazad_admin = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню админа')
    markup_nazad_admin.row(btn1)
    return markup_nazad_admin

def nazad_worker():
    markup_nazad_worker = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню воркера')
    markup_nazad_worker.row(btn1)
    return markup_nazad_worker


# Клавиатура с пополнением
def keyboard_balance_top_up_amount():
    markup = types.InlineKeyboardMarkup(row_width=0)
    for amount in ():
        callback_data = json.dumps({"amount": amount})
        markup.row(types.InlineKeyboardButton(f"{amount}",
                                              callback_data=callback_data))
    return markup

# Клавиатура с пополнением_2
def keyboard_balance_top_up_amount_2():
   markup_popolnenie = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
   btn1 = types.KeyboardButton('Проверить оплату')
   btn2 = types.KeyboardButton('Назад')
   markup_popolnenie.add(btn1, btn2)
   return markup_popolnenie


# Клавиатура с выводом
def keyboard_vivod():
    markup_vivod = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    markup_vivod.row(btn1)
    return markup_vivod


# Клавиатура администратора
def keyboard_admin():
    markup_admin = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Изменить баланс')
    btn2 = types.KeyboardButton('Сделать рассылку')
    btn3 = types.KeyboardButton('Изменить статус')
    btn4 = types.KeyboardButton('Добавить воркера')
    btn5 = types.KeyboardButton('Удалить воркера')
    btn6 = types.KeyboardButton('Информация')
    btn7 = types.KeyboardButton('Выйти')
    markup_admin.row(btn2)
    markup_admin.add(btn1, btn3)
    markup_admin.add(btn4, btn5)
    markup_admin.row(btn6)
    markup_admin.row(btn7)
    return markup_admin


# Клавитура воркера
def keyboard_worker():
    markup_worker = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Изменить баланс')
    btn2 = types.KeyboardButton('Вывести средства')
    btn3 = types.KeyboardButton('Информация')
    btn4 = types.KeyboardButton('Выйти')
    markup_worker.add(btn1, btn2)
    markup_worker.row(btn3)
    markup_worker.row(btn4)
    return markup_worker


# Клавиатура с исходом
def bet():
    markup_bet = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Кубик🎲')
    btn2 = types.KeyboardButton('Слоты🎰')
    btn3 = types.KeyboardButton('Рулетка🎡')
    btn4 = types.KeyboardButton('❌Закончить игру❌')
    markup_bet.add(btn1, btn2, btn3)
    markup_bet.row(btn4)
    return markup_bet
