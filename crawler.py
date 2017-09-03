import json
import sqlite3

import requests
import telegram
from tokens import tokens

DEBUG = False
CHANNEL_NAME = '@newsathlh' if not DEBUG else '@hlhstestchanel'
SOURCES = {
  'theverge': 'https://newsapi.org/v1/articles?source=the-verge&sortBy=top&apiKey=' + tokens['newsapi'],
  'theeconomist': 'https://newsapi.org/v1/articles?source=the-economist&sortBy=top&apiKey=' + tokens['newsapi']
}


def save_a_post(values, source):
  try:
    db.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?)',
               (values['author'], values['title'], values['description'],
                values['url'], values['urlToImage'], values['publishedAt'], source))
  except sqlite3.IntegrityError:
    return False
  return True


def send_to_channel(article):
  bot = telegram.Bot(tokens['bot'])
  bot.send_message(chat_id=CHANNEL_NAME, text="*{0}*\n{1}\n{2}".format(
    article['title'], article['description'],
    article['url']), parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True)


def send_unimportant(articles):
  art_to_post = []
  for art in articles:
    short = requests.post('https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyBCVSY8fbuu0vJaRGf0cpPuVf8M7e1d96Y',
                          data=json.dumps({'longUrl': art[0]['url']}), headers={'content-type': 'application/json'})
    short = short.content.decode('utf-8')
    print(short)
    short_url = json.loads(short)['id']
    art_to_post.append((art[0]['title'], short_url, art[1]))
  texts = ''
  for index, art in enumerate(art_to_post):
    texts += '*%s*' % str(index) + '. (%s)' % art[2][3] + art[0] + '  ' + \
             art[1] + '\n----------------------------------\n'
  # texts = [x[0] + ' ' + x[1] for x in art_to_post]
  # texts = '\n'.join(texts)
  bot = telegram.Bot(tokens['bot'])
  bot.send_message(chat_id=CHANNEL_NAME, text=texts, parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True,
                   disable_web_page_preview=True)


def get_posts():
  item_to_push = []
  candidate_item = []
  for source, url in SOURCES.items():
    print('now {0} - {1}'.format(source, url))
    result = requests.get(url).content.decode('utf-8')
    result = json.loads(result)
    for article in result['articles']:
      if save_a_post(article, source):
        if check_emergency(article['title']):
          item_to_push.append(article)
        else:
          candidate_item.append((article, source))
        print('{0} - {1}'.format(article['title'], source))
  list(map(send_to_channel, item_to_push))
  send_unimportant(candidate_item)


def check_emergency(title):
  word_list = ['Microsoft', 'Samsung', 'Windows', 'Google', 'Apple', 'Amazon', 'Facebook',
               'Snapchat', 'Tesla', 'Oneplus', 'Ameri', 'Linkin', 'Instagram',
               'Cana', 'Japan', 'Xiaomi', 'Football', 'Trump']
  for item in word_list:
    if item in title:
      return True
  return False


if __name__ == '__main__':
  db = sqlite3.connect('newsbase.sqlite3')
  get_posts()
  db.commit()
