import turingChat

from telegram.ext import Updater
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi')


def best(bot, update):
    bot.sendMessage(update.message.chat_id, text='Python is the best language ever.')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='This bot is created by Patrick Hao')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text[5:])


def chat(bot, update):
    chat_message = update.message.text[5:]
    send_message = turingChat.turning_chat(chat_message, turing_key)
    bot.sendMessage(update.message.chat_id, text=send_message)


def get_key():
    try:
        with open('key.txt') as key_file:
            tele_key = key_file.readline()
            turing_key = key_file.readline()
        return tele_key, turing_key
    except Exception as e:
        print(e)
        exit(0)


def main():
    my_updater = Updater(tele_key)
    dp = my_updater.dispatcher
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("best", best)
    dp.addTelegramCommandHandler("echo", echo)
    dp.addTelegramCommandHandler("chat", chat)

    my_updater.start_polling()
    my_updater.idle()


if __name__ == '__main__':
    tele_key, turing_key = get_key()
    tele_key = tele_key[:-1]
    main()
