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


def test(bot, update, args):
    chat_id = update.message.chat_id
    try:
        due = int(args[0])
        if due < 0:
            bot.sendMessage(chat_id, text='Sorry you can not go back to the future')

        def alarm(bot):
            bot.sendMessage(chat_id, text='Beep!')

        job_queue.put(alarm, due, repeat=False)
        bot.sendMessage(chat_id, text='Timer successfully set!')
    except IndexError:
        bot.sendMessage(chat_id, text='Usage: /set <seconds>')
    except ValueError:
        bot.sendMessage(chat_id, text='Usage: /set <seconds>')

        # bot.sendMessage(update.message.chat_id, text='%s' % update.message.chat_id)


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text[5:])


def chat(bot, update):
    chat_message = update.message.text[5:]
    send_message = turingChat.turning_chat(chat_message, turing_key)
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
                    'test': test,
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
