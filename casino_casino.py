import sqlite3
import random
from casino_config import bot, get_balance, get_last_popolnenie, get_status
from casino_keyboard import keyboard_osnova, keyboard_nazad, bet


# Казино начинает работу
def play_casino(message):
    balance = get_balance(message)
    bot.send_message(message.from_user.id, f"Введите сумму ставки💸 \n\nВаш баланс: {balance}0₽", reply_markup=keyboard_nazad())
    bot.register_next_step_handler(message, play_casino_2)


# Казино игра
def play_casino_2(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    balance = get_balance(message)

    if message.text == "❌Закончить игру❌":
        bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
                         reply_markup=keyboard_osnova())
        from casino_bot import get_text_message
        bot.register_next_step_handler(message, get_text_message)

    elif message.text.isdigit() and int(message.text) >= 0 and balance >= int(message.text):
        stavka = int(message.text)
        bot.send_message(message.from_user.id,
                         "Сейчас выпадет рандомное число от 1 до 99💎\n\nВыберите куда вложить🎲",
                         reply_markup=bet())
        bot.register_next_step_handler(message, play_casino_3, stavka)

    else:
        bot.send_message(message.from_user.id, "❌На Вашем счету недостаточно средств❌")
        play_casino(message)


# Казино игра
def play_casino_3(message, stavka):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    status = get_status(message)
    balance = get_balance(message)
    last_popolnenie = get_last_popolnenie(message)
    finish_popolnenie = last_popolnenie * 4.8
    if status != 0 and finish_popolnenie <= balance:
        status = 3
        cur.execute(f"UPDATE users SET status = {status} WHERE id = {message.chat.id}")
        con.commit()
    elif status == 3 and last_popolnenie * 4 >= balance:
        status = 2
        cur.execute(f"UPDATE users SET status = {status} WHERE id = {message.chat.id}")
        con.commit()

    else:
        pass

    stavka = stavka
    bet = message.text
    status = get_status(message)

    if bet == "Кубик🎲":

        if status == 0:
            number = random.choice(range(1, 50))
            if number < 50:
                bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                balance = balance - stavka + stavka * 2
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)
            else:
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 1:
            balances = balance - stavka + stavka * 2
            if balances < (last_popolnenie * 4.9):
                number = random.choice(range(1, 56))
                if number < 50:
                    bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                    balance = balance - stavka + stavka * 2
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
                else:
                    bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                    balance = balance - stavka
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
            else:
                number = random.choice(range(50, 100))
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 2:
            balances = balance - stavka + stavka * 2
            if balances < (last_popolnenie * 4.9):
                number = random.choice(range(20, 100))
                if number < 50:
                    bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                    balance = balance - stavka + stavka * 2
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
                else:
                    bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                    balance = balance - stavka
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
            else:
                number = random.choice(range(50, 100))
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 3:
            number = random.choice(range(50, 100))
            bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
            balance = balance - stavka
            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
            con.commit()
            play_casino(message)


    elif bet == "Слоты🎰":
        if status == 0:
            number = random.choice(range(50, 51))
            if number == 50:
                bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                balance = balance - stavka + stavka * 10
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)
            else:
                number = random.choice(range(1, 99))
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 1:
            balances = balance - stavka + stavka * 10
            if balances < (last_popolnenie * 4.9):
                number = random.choice(range(49, 51))
                if number == 50:
                    bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                    balance = balance - stavka + stavka * 10
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
                else:
                    number = random.choice(range(1, 99))
                    bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                    balance = balance - stavka
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
            else:
                number = random.choice(range(1, 50)) or random.choice(range(51, 99))
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 2:
            balances = balance - stavka + stavka * 10
            if balances < (last_popolnenie * 4.9):
                number = random.choice(range(40, 61))
                if number == 50:
                    bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                    balance = balance - stavka + stavka * 10
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
                else:
                    number = random.choice(range(1, 99))
                    bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                    balance = balance - stavka
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
            else:
                number = random.choice(range(1, 50)) or random.choice(range(51, 99))
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 3:
            number = random.choice(range(1, 50)) or random.choice(range(51, 99))
            bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
            balance = balance - stavka
            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
            con.commit()
            play_casino(message)


    elif bet == "Рулетка🎡":
        if status == 0:
            number = random.choice(range(50, 100))
            if number > 50:
                bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                balance = balance - stavka + stavka * 2
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)
            else:
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 1:
            balances = balance - stavka + stavka * 2
            if balances < (last_popolnenie * 4.9):
                number = random.choice(range(45, 100))
                if number > 50:
                    bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                    balance = balance - stavka + stavka * 2
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
                else:
                    bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                    balance = balance - stavka
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
            else:
                number = random.choice(range(1, 50))
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)

        elif status == 2:
            balances = balance - stavka + stavka * 2
            if balances < (last_popolnenie * 4.9):
                number = random.choice(range(1, 81))
                if number > 50:
                    bot.send_message(message.from_user.id, f"Вы выиграли! Выпало число {number}")
                    balance = balance - stavka + stavka * 2
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
                else:
                    bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                    balance = balance - stavka
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                    con.commit()
                    play_casino(message)
            else:
                number = random.choice(range(1, 50))
                bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_casino(message)


        elif status == 3:
            number = random.choice(range(1, 50))
            bot.send_message(message.from_user.id, f"Вы проиграли! Выпало число {number}")
            balance = balance - stavka
            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
            con.commit()
            play_casino(message)

    elif bet == "❌Закончить игру❌":
        bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
                         reply_markup=keyboard_osnova())
        from casino_bot import get_text_message
        bot.register_next_step_handler(message, get_text_message)