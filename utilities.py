import telegram
from tokens import tokens
import sqlite3

DEBUG = False
CHANNEL_NAME = '@newsathlh' if not DEBUG else '@hlhstestchanel'
db = sqlite3.connect('newsbase.sqlite3')
MESSAGE_LIMIT = 4


def send_to_channel(message: str, disable_preview=True):
  bot = telegram.Bot(tokens['bot'])
  message_sent = bot.send_message(chat_id=CHANNEL_NAME, text=message, parse_mode=telegram.ParseMode.MARKDOWN,
                                  disable_notification=True, disable_preview=disable_preview)
  handle_old_message(message_sent, message)


def delete_a_message(message_id: int):
  bot = telegram.Bot(tokens['bot'])
  bot.deleteMessage(chat_id=CHANNEL_NAME, message_id=message_id)


def save_a_message_record(new_message, message_content: str):
  db.execute('INSERT INTO messages VALUES (?,?,?,?)',
             (new_message.message_id, new_message.date, message_content, False))
  db.commit()


def delete_oldest_message():
  old_message = db.execute('SELECT message_id FROM messages WHERE messages.deleted =0 ORDER BY date ')
  # old_message = db.execute('SELECT * FROM messages')
  old_message = old_message.fetchall()
  old_message_len = len(old_message)
  if old_message_len > MESSAGE_LIMIT:
    db.execute('update messages set deleted=1 where message_id in '
               '(SELECT message_id from messages WHERE deleted=0 ORDER BY date LIMIT %s)' % (
                 old_message_len - MESSAGE_LIMIT))
    db.commit()
  for i in range(old_message_len - MESSAGE_LIMIT):
    delete_a_message(old_message[0][0])


def close_db_connect():
  db.close()


def handle_old_message(new_message, message_content: str):
  save_a_message_record(new_message, message_content)
  delete_oldest_message()


if __name__ == '__main__':
  send_to_channel("test4")
