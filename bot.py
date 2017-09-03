# from flask import Flask
# from flask import request
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from tokens import tokens

updater = Updater(token=tokens['bot'])
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # app = Flask(__name__)


def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="HLH 的新闻 Bot，一小时推送一次")
  bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


def echo(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
  bot.send_message(chat_id='@newsathlh', text=update.message.text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler('echo', echo))

updater.start_polling()
#
# if __name__ == '__main__':
#   app.run()
