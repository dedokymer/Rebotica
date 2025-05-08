# Практика: Решение задания 3
# Напиши Telegram бота, который будет выполнять роль таймера. Ему нужно будет отправить число в
# секундах и через столько секунд он снова напишет тебе. Если пользователь ввел не число, бот
# выдает предупреждение и просит заново ввести время. Для ожидания используй модуль time.

import time
import telebot
from my_token import TOKEN

bot = telebot.TeleBot(TOKEN)

mes = telebot.types.Message


@bot.message_handler(["start"])
def start(msg: mes):
    bot.send_message(msg.chat.id, "Привет! Я бот-таймер")
    question(msg)


def question(msg: mes):
    bot.send_message(msg.chat.id, "Через сколько секунд написать?")
    bot.register_next_step_handler(msg, number_check)


def number_check(msg: mes):
    if msg.text.isnumeric():
        time.sleep(int(msg.text))
        timer_end(msg, int(msg.text))
    else:
        bot.send_message(msg.chat.id, "Ты отправил не число! Пожалуйста, используй только числа!")
        question(msg)


def timer_end(msg: mes, sec: int):
    bot.send_message(msg.chat.id, f"Дзынь-Дзынь! {sec} секунд прошло!\n"
                                  f"Чтобы ещё раз воспользоваться мной, нажми /start")


bot.infinity_polling()

# Примечания:
# Проверка на число проводится с помощью метода .isnumeric(). Он возвращает True, если строка
# представляет собой число.
#
# Команда с сообщением «Через сколько секунд тебе написать?» специально вынесена в отдельную
# функцию, чтобы к ней можно было возвращаться и начинать опрос заново.
#
# Реализовать бота можно как угодно, скриншот всего лишь пример. Главное — полная работоспособность.
