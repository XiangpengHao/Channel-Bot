# from flask import Flask
# from flask import request
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from tokens import tokens
from  subprocess import call
from time import sleep
import os
import glob

RAID_PATH = "/mnt/raid1/hao/webcam/*.jpg"

updater = Updater(token=tokens['bot'])
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # app = Flask(__name__)


def take_photo(bot, update):
  print(update.message.chat_id)
  if update.message.chat_id not in tokens['allowed_id']:
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, not a chance.")
    return
  call(["curl", "-s", "-o", "/dev/null", "http://home.haoxp.xyz:7080/0/action/snapshot"])
  
  list_of_files = glob.glob(RAID_PATH)
  latest_file = max(list_of_files, key=os.path.getctime)
  
  bot.send_photo(chat_id=update.message.chat_id, photo=open(latest_file, 'rb'))


def echo(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
  bot.send_message(chat_id='@newsathlh', text=update.message.text)


start_handler = CommandHandler('shoot', take_photo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler('echo', echo))

updater.start_polling()
#
# if __name__ == '__main__':
#   app.run()
