from casino_config import bot, admin_1, admin_2, cashier, min_summa, fake_number, get_status, get_last_popolnenie, get_balance
from casino_keyboard import keyboard_osnova, keyboard_worker, keyboard_chifri, keyboard_vivod
from decimal import Decimal
from typing import Any
import sqlite3


def _create_invoice(amount: int) -> (str, int):
    """Creates an invoice for the amount.

    :param amount: invoice amount.
    :return: path for invoice, bill id.
    """
    invoice = cashier.create_bill(
        # Qiwi API requires amount with 2 signs after dot
        amount=Decimal(f"{amount}.00"),
        currency='RUB',
        comment='Casino invoice')
    return invoice.pay_url, invoice.bill_id


def _set_bill_id(user_id: int, bill_id: int) -> None:
    """Update bill id from user id

    :param user_id: telegram user id
    :param bill_id: bill id
    """
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET bill_id = ? WHERE id = ?", (bill_id, user_id))
    con.commit()


def _get_user_bill_id(user_id: int) -> Any:  # FIXME: replace Any to DB return type
    """Get bill_id from database by user_id

    :param user_id: telegram user id
    :return: Qiwi bill id
    """
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT bill_id FROM users WHERE id = {user_id}")
    return cur.fetchone()[0]


def _get_user_balance(user_id: int) -> int:
    """Get balance from user id

    :param user_id: telegram user id
    :return: user balance
    """
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = {user_id}")
    return cur.fetchone()[0]


def _top_up_balance(user_id: int, amount: int) -> None:
    """Top up balance from user id

    :param user_id: telegram user id
    """
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()


    cur.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (float(amount), user_id))
    con.commit()


    cur.execute(f"SELECT boss FROM users WHERE id = {user_id}")
    boss = cur.fetchone()[0]
    cur.execute(f"SELECT ref_balance FROM users WHERE id = {boss}")
    balance_ref = cur.fetchone()[0]
    balance_refs = balance_ref + float(amount) / 100 * 70
    cur.execute(f"UPDATE users SET ref_balance = {balance_refs} WHERE id = {boss}")
    con.commit()


def _reset_bill_id(user_id: int) -> None:
    """Top up balance from user id

    :param user_id: telegram user id
    """

    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"UPDATE users SET bill_id = NULL WHERE id = {user_id}")
    con.commit()


# Проверяется баланс для вывода
def vivod_money_1(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = {message.chat.id}")
    balance = cur.fetchone()[0]
    if message.text.isdigit() and balance >= int(message.text):
        vivod_money = int(message.text)
        bot.send_message(message.from_user.id,
                         "Выберите систему вывода из предложенных! \n\n"
                         "1)Банковская карта\n"
                         "2)Киви Кошелек\n"
                         "3)Яндекс Деньги\n"
                         "4)WebMoney\n"
                         "5)Bitcoin\n\n"
                         "Для выбора отправьте цифру, под которой указана нужная Вам система.", reply_markup=keyboard_chifri())
        bot.register_next_step_handler(message, vivod_money_2, vivod_money)

    elif message.text == "Назад":
        bot.send_message(message.from_user.id, "🔙 Вы вернулись в главное меню", reply_markup=keyboard_osnova())

    else:
        bot.send_message(message.from_user.id, "Упс, что-то пошло не так :(")


# Берем номер счета
def vivod_money_2(message, vivod_money):
    sposop = message.text
    bot.send_message(message.from_user.id, "💵Введите реквизиты кошелька для вывода средств!💵 \n\n⚠Ваша заявка будет принята после осмотра модератором!⚠", reply_markup=keyboard_vivod())
    bot.register_next_step_handler(message, vivod_money_3, vivod_money, sposop)


# Функция, которая приняла номер для вывода
def vivod_money_3(message, vivod_money, sposob):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    status = get_status(message)
    sposob = sposob
    akkaunt_user = message.chat.id
    number = message.text
    if status == 0:
        if number == fake_number:

            cur.execute(f"SELECT balance FROM users WHERE id = {message.chat.id}")
            balance = cur.fetchone()[0]
            balance = balance - int(vivod_money)
            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
            con.commit()
            status = 1
            cur.execute(f"UPDATE users SET status = {status} WHERE id = {message.chat.id}")
            con.commit()
            bot.send_message(message.from_user.id,
                             "Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут. \nОжидайте!")


        elif number != fake_number:
            bot.send_message(message.chat.id,
                             "⚠Ваша заявка будет принята после осмотра модератором!⚠")

    else:
        last_popolnenie = get_last_popolnenie(message)
        balance = get_balance(message)
        req_balance = last_popolnenie * 5 - balance
        bot.send_message(message.chat.id,
                         f"😔 Упс, недостаточно средств 😔\n\n❗ Вывод возможен только в том случае, если Ваш наигранный баланс >= (Последнее пополнение * 5) ❗\n\n💸 Последнее пополнение {last_popolnenie}₽ 💸\n\n💵 Ваш баланс {balance}₽ 💵\n\n💰Необходимый выиграть еще {req_balance}₽ для вывода средств💰\n")


# Вывод воркерам
def worker_zp(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT ref_balance FROM users WHERE id = {message.chat.id}")
    ref_balance = cur.fetchone()[0]
    if message.text.isdigit() and ref_balance >= int(message.text) and int(message.text) >= min_summa:
        vivod_money = int(message.text)
        bot.send_message(message.from_user.id,
                         "Выберите систему вывода из предложенных! \n\n"
                         "1)Банковская карта\n"
                         "2)Киви Кошелек\n"
                         "3)Яндекс Деньги\n"
                         "4)WebMoney\n"
                         "5)Bitcoin\n\n"
                         "Для выбора отправьте цифру, под которой указана нужная Вам система.", reply_markup=keyboard_chifri())
        bot.register_next_step_handler(message, worker_zp_2, vivod_money)

    elif message.text == "Назад":
        bot.send_message(message.from_user.id, "🔙 Вы вернулись в главное меню", reply_markup=keyboard_worker())
        from casino_bot import get_text_message_worker
        bot.register_next_step_handler(message, get_text_message_worker)

    else:
        bot.send_message(message.from_user.id, "Упс, что-то пошло не так :(")
        from casino_bot import get_text_message_worker
        bot.register_next_step_handler(message, get_text_message_worker)


# Вывод вркерам_2
def worker_zp_2(message, vivod_money):
    sposop = int(message.text)
    bot.send_message(message.from_user.id, "💵Введите реквизиты кошелька для вывода средств!💵", reply_markup=keyboard_vivod())
    bot.register_next_step_handler(message, worker_zp_3, vivod_money, sposop)


# Вывод воркерам_3
def worker_zp_3(message, vivod_money, sposob):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    sposob = sposob
    if sposob == 1:
        sposob = "Банковская карта"
    elif sposob == 2:
        sposob = "Киви Кошелек"
    elif sposob == 3:
        sposob = "Яндекс Деньги"
    elif sposob == 4:
        sposob = "WebMoney"
    elif sposob == 5:
        sposob = "Bitcoin"
    akkaunt_user = message.chat.id
    number = message.text
    cur.execute(f"SELECT ref_balance FROM users WHERE id = {message.chat.id}")
    ref_balance = cur.fetchone()[0]
    ref_balance = ref_balance - int(vivod_money)
    cur.execute(f"UPDATE users SET ref_balance = {ref_balance} WHERE id = {message.chat.id}")
    con.commit()
    bot.send_message(message.from_user.id,
                             "Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут. \nОжидайте!")

    bot.send_message(admin_1, f"Пользователь: {akkaunt_user}\n"
                            f"Реквизиты: {sposob}\n"
                            f"Номер счета: {number}\n"
                            f"Сумма: {vivod_money}\n")
    bot.send_message(admin_2, f"Пользователь: {akkaunt_user}\n"
                              f"Реквизиты: {sposob}\n"
                              f"Номер счета: {number}\n"
                              f"Сумма: {vivod_money}\n")

    from casino_bot import get_text_message_worker
    bot.register_next_step_handler(message, get_text_message_worker)
