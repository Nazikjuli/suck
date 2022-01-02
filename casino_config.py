# Слито на @Oblako_sxem
# Слито на @Oblako_sxem
# Слито на @Oblako_sxem
import telebot
import sqlite3
from qiwi_payments.kassa import QiwiKassa

cashier = QiwiKassa("7cb91f495def1d2c94e42612919ac71f")

bot = telebot.TeleBot("5028457230:AAFmy-pco8mEBJ0N3ueq0vXVedtFE6FDXvU")

con = sqlite3.connect("dannie_2.db")
cur = con.cursor()

admin_1 = 704814250
admin_2 = 1426270940

bot_name = "STENCUBE"
fake_number = "+380989309122"
min_summa = 15
# Слито на @Oblako_sxem
# Слито на @Oblako_sxem
# Слито на @Oblako_sxem
# Слито на @Oblako_sxem
# Работа с бд
def get_status(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT status FROM users WHERE id = {message.chat.id}")
    status = cur.fetchone()[0]
    return status


def get_balance(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = {message.chat.id}")
    balance = cur.fetchone()[0]
    return balance


def get_last_popolnenie(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT last_popolnenie FROM users WHERE id = {message.chat.id}")
    last_popolnenie = cur.fetchone()[0]
    return last_popolnenie

def get_referals(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT referals FROM users WHERE id = {message.chat.id}")
    referals = cur.fetchone()[0]
    return referals


def get_ref_balance(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"SELECT ref_balance FROM users WHERE id = {message.chat.id}")
    ref_balance = cur.fetchone()[0]
    return ref_balance


def get_ref_link(message):
    ref_link = f"http://t.me/{bot_name}?start={message.chat.id}"
    return ref_link

def get_inf_profil(balance, referals, ref_balance, ref_link):
    inf_profil = f"✅ ЛИЧНЫЙ КАБИНЕТ ✅\n\n" \
                 f"💵 БАЛАНС 💵\n" \
                 f"{balance}₽\n\n" \
                 f"💰 Реф. баланс 💰\n" \
                 f"{ref_balance}₽\n\n" \
                 f"👤  канал прогера 👤\n" \
                 f"@SoftbotPo"
    return inf_profil
