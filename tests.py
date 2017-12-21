from Bot import Bot, BotType
from NewsProvider import NewsProvider
import os

CHANNEL_NAME = '@hlhstestchanel' if ('BOT_DEBUG' in os.environ) else '@newsathlh'


def test1():
  bot = Bot(CHANNEL_NAME)
  message_sent = bot.send_message("test message 3")
  # pass
  bot.delete_message(message_id=message_sent.message_id - 1)


def test2():
  news = NewsProvider()
  result = news.get_send_message()
  print(result)


def test3():
  news = NewsProvider()
  rv = news.get_send_message()
  with Bot(CHANNEL_NAME) as bot:
    important = rv['important']
    unimportant = rv['unimportant']
    for item in important:
      bot.send_message(item)
    for item in unimportant:
      bot.send_message(item, disable_preview=True, disable_notification=True, disable_web_page_preview=True)


if __name__ == '__main__':
  test3()
