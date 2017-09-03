import json
import pytz
from datetime import datetime
import requests
import telegram

from tokens import tokens

DEBUG = False
CHANNEL_NAME = '@newsathlh' if not DEBUG else '@hlhstestchanel'
WEATHER_CODE = {
  1003: '🌤',
  1006: '🌥',
  1009: '☁️',
  1063: '🌨',
  1066: '❄️',
  1087: '⚡️',
  1114: '❄️'
}
CITY_CONFIGS = [
  {'name': 'Vancouver', 'timezone': 'Canada/Pacific'},
  {'name': 'Hangzhou', 'timezone': 'Asia/Shanghai'}
]


def get_local_time(timezone: str):
  local_time = datetime.now(pytz.timezone(timezone))
  return '{:%H:%M}'.format(local_time)


def get_weather() -> str:
  weather_texts = ''
  for city in CITY_CONFIGS:
    weather_texts += '*{0} ({1})*\n'.format(city['name'], get_local_time(city['timezone']))
    forecast = requests.get(
      'https://api.apixu.com/v1/forecast.json?key={0}&q={1}'.format(tokens['weather'], city['name']))
    forecast = forecast.content.decode()
    forecast = json.loads(forecast)
    weather_today = forecast['forecast']['forecastday'][0]
    weather_texts += 'Max temp: ' + str(weather_today['day']['maxtemp_c']) + \
                     '\nMin temp: ' + str(weather_today['day']['mintemp_c']) + \
                     '\nHumidity: ' + str(weather_today['day']['avghumidity']) + \
                     '\nCondition: ' + weather_to_emoji(weather_today['day']['condition']['code'])
    weather_texts += '\n====================\n'
  return weather_texts


def send_message(text: str):
  bot = telegram.Bot(tokens['bot'])
  bot.send_message(chat_id=CHANNEL_NAME, text=text, parse_mode=telegram.ParseMode.MARKDOWN,
                   disable_notification=True)


def weather_to_emoji(code: int) -> str:
  if code == 1000:
    return '☀️'
  elif code == 1003:
    return '🌤'
  elif code == 1006:
    return '🌥'
  elif code == 1009:
    return '☁️'
  elif code == 1063:
    return '🌨'
  elif code == 1066:
    return '❄️'
  else:
    return '🌚(%s)' % code
  pass


if __name__ == '__main__':
  weather = get_weather()
  send_message(weather)
  # print(get_local_time('Canada/Pacific'))
