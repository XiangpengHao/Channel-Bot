from telegram import Updater
import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
logger =logging.getLogger(__name__)

def start(bot,update):
    bot.sendMessage(update.message.chat_id,text='Hi')

def best(bot,update):
    bot.sendMessage(update.message.chat_id,text='Python is the best language ever.')

def help(bot,update):
    bot.sendMessage(update.message.chat_id,text='This bot is created by Patrick Hao')

def echo(bot,update):
    bot.sendMessage(update.message.chat_id,text=update.message.text[5:])

def main():
    updater=Updater("149794753:AAEv4zJDt5IPY-A8sBEwo5I2p_9MT_TldZw")
    dp=updater.dispatcher
    dp.addTelegramCommandHandler("start",start)
    dp.addTelegramCommandHandler("help",help)
    dp.addTelegramCommandHandler("best",best)
    dp.addTelegramCommandHandler("echo",echo)

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
