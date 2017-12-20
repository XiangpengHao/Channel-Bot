from Bot import Bot
from NewsProvider import NewsProvider
from WeatherProvider import WeatherProvider
import os, sys

CHANNEL_NAME = '@hlhstestchanel' if ('BOT_DEBUG' in os.environ) else '@newsathlh'


def clean_message(bot):
  bot.clean_channel()


def send_news(bot):
  news = NewsProvider()
  rv = news.get_send_message()
  
  important = rv['important']
  unimportant = rv['unimportant']
  for item in important:
    if not item: continue
    bot.send_message(item)
  for item in unimportant:
    if not item: continue
    bot.send_message(item, disable_web_page_preview=True)


def send_weather(bot):
  weather = WeatherProvider()
  rv = weather.get_all_weather()
  bot.send_message(rv)


if __name__ == '__main__':
  with Bot(CHANNEL_NAME) as bot:
    if sys.argv[1] == 'all':
      send_news(bot)
      send_weather(bot)
    elif sys.argv[1] == 'news':
      send_news(bot)
    elif sys.argv[1] == 'weather':
      send_weather(bot)
    
    clean_message(bot)
