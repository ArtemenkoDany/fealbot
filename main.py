from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import sqlite3

import asyncio
import aioschedule
import random

button1 = KeyboardButton('счастье 😀')
button2 = KeyboardButton('грусть 😔')
button3 = KeyboardButton('испуг/удивление 😳')
button4 = KeyboardButton('гнев/отвращение 😡')

button5 = KeyboardButton("Нет, не нужно")
button6 = KeyboardButton("Да, давай")


markup1 = ReplyKeyboardMarkup(one_time_keyboard=True).add(button5).add(button6)
markup3 = ReplyKeyboardMarkup(one_time_keyboard=True).add(button1).add(button2).add(button3).add(button4)

TOKEN = '5204075373:AAFSSBvj_9mAg7wmBsVmVlu8RdQsrjofJew'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def max_user_id(self):
        result = self.cursor.execute("SELECT max(`id`) FROM `users`")
        return result.fetchone()[0]

    def get_id(self):
        result = self.cursor.execute("SELECT `user_id` FROM `users` ORDER BY `id` ")
        return result.fetchall()

    def add_user(self, user_id, name):
        self.cursor.execute("INSERT INTO `users` (`user_id`, `name`, `feal1`, `feal2`,`feal3`,`feal4`) VALUES (?,?,?,?,?,?) ", (user_id, name, 0, 0 ,0 , 0,))
        return self.conn.commit()

    def add_user_feal1(self, user_id):
      self.cursor.execute("UPDATE `users` SET `feal1` = `feal1`+1 WHERE `user_id` = ?", (user_id,))
      return self.conn.commit()

    def add_user_feal2(self, user_id):
        self.cursor.execute("UPDATE `users` SET `feal2` = `feal2`+1 WHERE `user_id` = ?", (user_id,))
        return self.conn.commit()

    def add_user_feal3(self, user_id):
        self.cursor.execute("UPDATE `users` SET `feal3` = `feal3`+1 WHERE `user_id` = ?", (user_id,))
        return self.conn.commit()

    def add_user_feal4(self, user_id):
        self.cursor.execute("UPDATE `users` SET `feal4` = `feal4`+1 WHERE `user_id` = ?", (user_id,))
        return self.conn.commit()

    def feal_stat(self):
        result = self.cursor.execute("SELECT max(feal1, feal2, feal3, feal4) FROM users")
        return result.fetchall()

    def feal_array(self):
        result = self.cursor.execute("SELECT `feal1`, `feal2`,`feal3`,`feal4` FROM `users`")
        return result.fetchall()

    def feal_zero(self, user_id):
        self.cursor.execute("UPDATE `users` SET `feal1` = 0 , `feal2` = 0 ,`feal3` = 0, `feal4` = 0  WHERE `user_id` = ?", (user_id,))
        return self.conn.commit()

BotDB = BotDB("C:/Users/dan02/OneDrive/Desktop/botfeal.db")

user_id = BotDB.get_id()

ud= [x for t in user_id for x in t]

spisok= []
q = 0
w = 0

for c in BotDB.feal_array():
    q=q+1
    for z in BotDB.feal_stat():
        w=w+1
        if q==w:
            if z[0] == c[0]:
                spisok.append(f'Ура, на этой неделе преобладала эмоция счастья! Чем была ценна для тебя эта неделя?')
            elif z[0] == c[1]:
                spisok.append(f'Почему так много грустишь? Может есть что-то, что могло бы тебя порадовать?\nУлыбнись!')
            elif z[0] == c[2]:
                spisok.append(f"Что вызывало у тебя тревогу на этой неделе?\nМожешь попробовать помедитировать на следующей неделе, чтобы тревога всё реже появлялась в твоей жизни")
            elif z[0] == c[3]:
                spisok.append(f"На этой неделе ты чаще всего испытывал эмоцию злости, может нужно немного отдохнуть, чтобы раздражение ушло?")
    q=q+BotDB.max_user_id()

spud = dict(zip(ud, spisok))

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id, message.from_user.first_name)

    await message.reply(f"Привет, {message.from_user.first_name}!\nЯ бот, который поможет тебе отслеживать эмоции.\nМожешь попробовать описать свое состояние уже сейчас:", reply_markup=markup3)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!", reply_markup=markup3)


@dp.message_handler(content_types=['text'], text="счастье 😀")
async def handler(message: types.Message):
     await message.answer(f'{message.from_user.first_name}, я добавил твою эмоцию: счастье 😀')
     if BotDB.get_user_id(message.from_user.id):
         BotDB.add_user_feal1(message.from_user.id)

@dp.message_handler(content_types=['text'], text="грусть 😔")
async def handler(message: types.Message):
     await message.answer(f'{message.from_user.first_name}, я добавил твою эмоцию: грусть 😔\nХочу тебе напомнить, что ощущая грусть ты можешь познавать краски жизни!\nТы справишься, в конце концов ты всегда справлялся')
     if BotDB.get_user_id(message.from_user.id):
         BotDB.add_user_feal2(message.from_user.id)
     await bot.send_message(message.from_user.id, "Что тебя так огорчило, может хочешь посмотреть на рандомного котика что бы поднять себе настроение?", reply_markup=markup1)

@dp.message_handler(content_types=['text'], text="испуг/удивление 😳")
async def handler(message: types.Message):
     await message.answer(f'{message.from_user.first_name}, я добавил твою эмоцию: испуг/удивление 😳\nКак ты думаешь, почему ты сейчас испытываешь тревогу?\nЧтобы отвлечься советую сделать 5 вдохов-выдохов сконцентрировавшись на них.')
     if BotDB.get_user_id(message.from_user.id):
         BotDB.add_user_feal3(message.from_user.id)

@dp.message_handler(content_types=['text'], text="гнев/отвращение 😡")
async def handler(message: types.Message):
     await message.answer(f'{message.from_user.first_name}, я добавил твою эмоцию: гнев/отвращение 😡')
     if BotDB.get_user_id(message.from_user.id):
         BotDB.add_user_feal4(message.from_user.id)

@dp.message_handler(content_types=['text'], text="Нет, не нужно")
async def handler(message: types.Message):
     await message.answer("Ладно, но ты все же не грусти)")

@dp.message_handler(content_types=['text'], text="Да, давай")
async def handler(message: types.Message):
    await bot.send_photo(message.from_user.id, "https://thiscatdoesnotexist.com")


async def noon_print():
    for z in range(len(BotDB.get_id())):
        await bot.send_message(BotDB.get_id()[z][0], "Расскажи о своих эмоциях:", reply_markup=markup3)



async def stat_print():
    for z in range(len(BotDB.get_id())):
        await bot.send_message(BotDB.get_id()[z][0], spud[BotDB.get_id()[z][0]])
        BotDB.feal_zero(BotDB.get_id()[z][0])

x = random.randint(6, 10)
y = random.randint(11, 16)
z = random.randint(17, 22)
v = random.randint(11, 59)

async def scheduler():
    aioschedule.every().day.at(str(x)+":"+str(v)).do(noon_print)
    aioschedule.every().day.at(str(y)+":"+str(v)).do(noon_print)
    aioschedule.every().day.at(str(z)+":"+str(v)).do(noon_print)
    aioschedule.every().friday.at("12:00").do(stat_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)

