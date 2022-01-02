import sqlite3
import time
from casino_config import bot, admin_1, admin_2
from casino_keyboard import keyboard_admin, keyboard_worker


# Рассылка сообщений
def admin_rassilka(message):
    rassilka = message.text
    bot.send_message(message.from_user.id,
                     'Запустить рассылку? Введите "Да", чтобы начать рассылку, либо же "Нет", чтобы отменить ее')
    bot.register_next_step_handler(message, admin_rassilka2, rassilka)


# Рассылка сообщений_2
def admin_rassilka2(message, rassilka):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    if message.text == "Да":
        bot.send_message(message.from_user.id, "Рассылка началась", reply_markup=keyboard_admin())
        cur.execute("SELECT id FROM users")
        id = cur.fetchall()
        for id in id:
            for id in id:
               try:
                bot.send_message(id, f"{rassilka}")
                time.sleep(1)
               except:
                   pass
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)

    else:
        bot.send_message(message.from_user.id, "Рассылка отменена", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)


# Изменение баланса
def chan_balance(message):

    try:
        id = int(message.text)
        bot.send_message(message.from_user.id, "Введите, какой баланс сделать человеку")
        bot.register_next_step_handler(message, chan_balance_2, id)

    except:
       if message.chat.id == admin_1 or message.chat.id == admin_2:

        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)

       else:

           bot.send_message(message.from_user.id, "Вы вернулись в меню воркера", reply_markup=keyboard_worker())
           from casino_bot import get_text_message_worker
           bot.register_next_step_handler(message, get_text_message_worker)



# Изменение баланса_2
def chan_balance_2(message, id):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    try:
        balance = int(message.text)
        id = id

        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {id}")
        con.commit()
        if message.chat.id == admin_1 or message.chat.id == admin_2:

            bot.send_message(message.from_user.id, "Баланс успешно изменен", reply_markup=keyboard_admin())

            from casino_bot import get_text_message_admin

            bot.register_next_step_handler(message, get_text_message_admin)


        else:

            bot.send_message(message.from_user.id, "Баланс успешно изменен", reply_markup=keyboard_worker())

            from casino_bot import get_text_message_worker

            bot.register_next_step_handler(message, get_text_message_worker)

    except:
        if message.chat.id == admin_1 or message.chat.id == admin_2:

            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)

        else:

            bot.send_message(message.from_user.id, "Вы вернулись в меню воркера", reply_markup=keyboard_worker())
            from casino_bot import get_text_message_worker
            bot.register_next_step_handler(message, get_text_message_worker)


# Изменение статуса
def chan_status(message):

    try:
        id = int(message.text)
        bot.send_message(message.from_user.id,
                         "Введите, какой статус сделать человеку (0 - Премиум, 1 - Азарт) * Лучше вообще не трогать")
        bot.register_next_step_handler(message, chan_status_2, id)
    except:

            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)




# Изменение статуса_2
def chan_status_2(message, id):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    try:
        status = int(message.text)
        id = id
        if status == 0 or status == 1 or status == 2:

            try:
                cur.execute(f"UPDATE users SET status = {status} WHERE id = {id}")
                con.commit()
                bot.send_message(message.from_user.id, "Статус успешно изменен",  reply_markup=keyboard_admin())
                from casino_bot import get_text_message_admin
                bot.register_next_step_handler(message, get_text_message_admin)
            except:
                bot.send_message(message.from_user.id, "Вы вернулись в меню админа",  reply_markup=keyboard_admin())
                from casino_bot import get_text_message_admin
                bot.register_next_step_handler(message, get_text_message_admin)

        else:
            bot.send_message(message.from_user.id, "Такой статус невозможно сделать",  reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)

    except:

        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())

        from casino_bot import get_text_message_admin

        bot.register_next_step_handler(message, get_text_message_admin)



# Сделать воркером
def ins_workers(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()

    try:
        id = int(message.text)
        cur.execute(f"INSERT INTO workers (id) VALUES (\"{id}\")")
        con.commit()
        bot.send_message(message.from_user.id, "Воркер успешно добавлен", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)
    except:
        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)


# Удалить из воркеров
def del_workers(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()

    try:
        id = int(message.text)
        cur.execute(f"DELETE FROM workers WHERE id = {id}")
        con.commit()
        bot.send_message(message.from_user.id, "Воркер успешно удален", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)
    except:
        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)


