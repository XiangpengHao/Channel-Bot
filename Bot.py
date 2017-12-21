import telegram
from telegram import TelegramError
from config import tokens
from Connection import ConnectionChannel
from typing import List


class Bot():
  def __init__(self, channel_name: str) -> None:
    self._bot: telegram.Bot = telegram.Bot(tokens['bot'])
    self._connection = ConnectionChannel()
    self._channel_name: str = channel_name
  
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    self._connection.close()
  
  def send_message(self, message: str, disable_notification=True, disable_preview=True,
                   disable_web_page_preview=False) -> telegram.Message:
    message_sent: telegram.Message = self._bot.send_message(
      chat_id=self._channel_name, text=message, parse_mode=telegram.ParseMode.MARKDOWN,
      disable_notification=disable_notification, disable_preview=disable_preview,
      disable_web_page_preview=disable_web_page_preview
    )
    self._connection.insert_message(message_sent.message_id, message_sent.date, message, self._channel_name)
    return message_sent
  
  def delete_message(self, message_id: int) -> bool:
    self._connection.mark_delete(message_id=message_id, channel_name=self._channel_name)
    try:
      result = self._bot.delete_message(chat_id=self._channel_name, message_id=message_id)
    except TelegramError as e:
      print(e)
      return False
    return result
  
  def clean_channel(self):
    yesterday_not_deleted: List[int] = self._connection.get_yesterday_not_deleted(self._channel_name)
    for message in yesterday_not_deleted:
      self.delete_message(message_id=message)
  
  def close_connection(self):
    self._connection.close()

# usage:
# with Bot(channel_name) as bot:
#   bot.foo()
# @contextlib.contextmanager
# def Bot(channel_name: str) -> Callable[[str], BotType]:
#   tg_bot = BotType(channel_name=channel_name)
#   yield tg_bot
#   tg_bot.close_connection()
