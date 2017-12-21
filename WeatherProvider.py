import requests, json, sys
from config import WEATHER_URL, CITY_CONFIG, tokens
from typing import Dict


class WeatherProvider():
  def __init__(self, city_config=CITY_CONFIG):
    self._city_config: Dict[str, str] = city_config
    self._weather_info: Dict = {}
    self._sensor_info: Dict[str, float] = {}
  
  def _get_weather_from_web(self) -> dict:
    for city, id in self._city_config.items():
      weather_url = WEATHER_URL + '&id={id}&appid={appid}'.format(id=id, appid=tokens['open_weather'])
      rv = requests.get(weather_url).content.decode()
      rv: Dict = json.loads(rv)
      self._weather_info[city] = rv
    return self._weather_info
  
  def _get_weather_from_sensor(self) -> dict:
    try:
      import Adafruit_DHT
      hum, temp = Adafruit_DHT.read_retry(11, 4)
    except ImportError:
      hum, temp = -1, -1
    self._sensor_info['temp'] = temp
    self._sensor_info['hum'] = hum
    return self._sensor_info
  
  def _format_all(self) -> str:
    rv: str = ''
    for city, weather in self._weather_info.items():
      rv += self._format_one_web_weather(weather)
      rv += '\n----------------\n'
    rv += self._format_sensor_weather()
    return rv
  
  def _format_one_web_weather(self, weather_item: dict) -> str:
    return '*{city}*\n' \
           'Max temp: {max_temp}°C\n' \
           'Min temp: {min_temp}°C\n' \
           'Humidity: {hum}%\n' \
           'Condition: {condition}'.format(
      city=weather_item['name'], max_temp=weather_item['main']['temp_max'], min_temp=weather_item['main']['temp_min'],
      hum=weather_item['main']['humidity'], condition=weather_item['weather'][0]['description']
    )
  
  def _format_sensor_weather(self) -> str:
    return '*Patrick\'s Home*\nTemp: {temp}°C\nHumidity: {humidity}%'.format(
      temp=self._sensor_info['temp'], humidity=self._sensor_info['hum']
    )
  
  def get_all_weather(self):
    self._get_weather_from_sensor()
    self._get_weather_from_web()
    return self._format_all()
