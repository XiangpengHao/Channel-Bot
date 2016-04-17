import turingChat

from telegram.ext import Updater
import telegram
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi')


def best(bot, update):
    bot.sendMessage(update.message.chat_id, text='Python is the best language ever.')


def study(bot, update, args):
    chat_id = update.message.chat_id
    try:
        due = int(args[0])
        if due < 0:
            bot.sendMessage(chat_id, text='好好學習！！！！')

        def alarm(bot):
            bot.sendMessage(chat_id, text='時間到啦，可以休息一會')

        job_queue.put(alarm, due, repeat=False)
        bot.sendMessage(chat_id, text='%s 開始學習了呢, %s秒以後再來找我哦'%(update.message.from_user.username,due))
    except IndexError:
        bot.sendMessage(chat_id, text='Usage: /study <seconds> \n設置學習時間\n好好學習，自習滿績人生巔峯！')
    except ValueError:
        bot.sendMessage(chat_id, text='Usage: /study <seconds> \n設置學習時間\n好好學習，自習滿績人生巔峯！')

        # bot.sendMessage(update.message.chat_id, text='%s' % update.message.chat_id)


def echo(bot, update, args):
    if len(args[0]):
        send_message = 'Usage: /echo <message>'
    else:
        send_message = args[0]
    bot.sendMessage(update.message.chat_id, text=send_message)


def chat(bot, update, args):
    if len(args[0]):
        send_message = 'Usage: /chat <chat message>'
    else:
        send_message = turingChat.turning_chat(update.message.text[5:], turing_key)
    bot.sendMessage(update.message.chat_id, text=send_message)


def worst(bot, update):
    bot.sendMessage(update.message.chat_id, text='PHP is the worst language ever!!!!!!!!!')


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
    global tele_key, turing_key, job_queue
    tele_key, turing_key = get_key()
    tele_key = tele_key[:-1]

    my_updater = Updater(tele_key)
    job_queue = my_updater.job_queue
    dp = my_updater.dispatcher

    command_list = {'start': start,
                    'study': study,
                    'best': best,
                    'worst': worst,
                    'echo': echo,
                    'chat': chat}

    for (command, function) in command_list.items():
        dp.addTelegramCommandHandler(command, function)

    my_updater.start_polling()
    my_updater.idle()


if __name__ == '__main__':
    main()
