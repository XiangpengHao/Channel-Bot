import telegram, contextlib
from config import tokens
from Connection import ConnectionChannel
from typing import List


# usage:
# with Bot(channel_name) as bot:
#   bot.foo()
@contextlib.contextmanager
def Bot(channel_name: str):
  class Bot():
    def __init__(self, channel_name: str):
      self._bot: telegram.Bot = telegram.Bot(tokens['bot'])
      self._connection = ConnectionChannel()
      self._channel_name: str = channel_name
    
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
      return self._bot.delete_message(chat_id=self._channel_name, message_id=message_id)
    
    def clean_channel(self):
      yesterday_not_deleted: List[int] = self._connection.get_yesterday_not_deleted(self._channel_name)
      for message in yesterday_not_deleted:
        self.delete_message(message_id=message)
    
    def close_connection(self):
      self._connection.close()
  
  tg_bot = Bot(channel_name=channel_name)
  yield tg_bot
  tg_bot.close_connection()
