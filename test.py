from Bot import Bot
import os

CHANNEL_NAME = '@hlhstestchanel' if ('BOT_DEBUG' in os.environ) else '@newsathlh'


def test():
  bot = Bot(CHANNEL_NAME)
  message_sent = bot.send_message("test message 4")
  # pass
  bot.delete_message(message_id=message_sent.message_id - 1)


if __name__ == '__main__':
  test()
