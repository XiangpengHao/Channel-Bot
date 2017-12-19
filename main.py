from Bot import Bot
from NewsProvider import NewsProvider
import os, sys

CHANNEL_NAME = '@hlhstestchanel' if ('BOT_DEBUG' in os.environ) else '@newsathlh'


def clean_message():
  with Bot(CHANNEL_NAME) as bot:
    bot.clean_channel()


def send_news():
  news = NewsProvider()
  rv = news.get_send_message()
  with Bot(CHANNEL_NAME) as bot:
    important = rv['important']
    unimportant = rv['unimportant']
    for item in important:
      bot.send_message(item)
    for item in unimportant:
      bot.send_message(item, disable_preview=True, disable_notification=True, disable_web_page_preview=True)


def send_weather():
  pass


if __name__ == '__main__':
  if sys.argv[1] == 'all':
    send_news()
    send_weather()
  elif sys.argv[1] == 'news':
    send_news()
  elif sys.argv[1] == 'weather':
    send_weather()
  
  clean_message()
