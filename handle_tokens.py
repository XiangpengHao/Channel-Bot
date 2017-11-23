import sqlite3
import nltk
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from datetime import datetime
import math

SIGMA = 30

RATIO_ECON = 1.1
RATIO_TITLE = 1.4

db = sqlite3.connect('newsbase.sqlite3')


def tokenize_and_stem(text: str) -> list:
  tokens = nltk.word_tokenize(text)
  return [EnglishStemmer(ignore_stopwords=True).stem(x) for x in tokens]


def eliminate_stop_words(tokens: list) -> list:
  stop_word = set(stopwords.words('english'))
  return [x.lower() for x in tokens if x.lower() not in stop_word and len(x) > 2]


def save_or_update_token(token: dict):
  cursor = db.cursor()
  cursor.execute('SELECT * FROM tokens WHERE token =?', (token['value'],))
  
  data = cursor.fetchone()
  if data:
    cursor.execute('UPDATE tokens SET occr_e=?, occr_v=?,occr_t=?,occr_d=?,date=? WHERE token=?',
                   (data[1] + (0 if token['is_verge'] else 1),
                    data[2] + (1 if token['is_verge'] else 0),
                    data[4] + (1 if token['is_title'] else 0),
                    data[5] + (0 if token['is_title'] else 1),
                    data[0], str(datetime.now())))
  else:
    cursor.execute('INSERT INTO tokens(token, occr_t, occr_d, occr_e, occr_v) VALUES (?,?,?,?,?)',
                   (token['value'], 1 if token['is_title'] else 0, 0 if token['is_title'] else 1,
                    0 if token['is_verge'] else 1, 1 if token['is_verge'] else 0))


def handle_text(text: str, is_title: bool, is_verge: bool) -> list:
  tokens = tokenize_and_stem(text)
  tokens = eliminate_stop_words(tokens)
  return [{'value': x, 'is_title': is_title, 'is_verge': is_verge} for x in tokens]


def read_all_posts() -> list:
  all_posts = db.execute('SELECT title,description,source FROM posts')
  all_posts = all_posts.fetchall()
  return all_posts


def run_all(all_posts):
  flatten = lambda x: [item for sublist in x for item in sublist]
  all_title_dicts = flatten([handle_text(post[0], True, post[2] == 'theverge') for post in all_posts])
  all_desc_dicts = flatten([handle_text(post[1], False, post[2] == 'theverge') for post in all_posts])
  all_title_dicts.extend(all_desc_dicts)
  list(map(lambda x: save_or_update_token(x), all_title_dicts))
  db.commit()


def query_token(token: str) -> tuple:
  token_info = db.execute('SELECT occr_e,occr_v,occr_t,occr_d,date FROM tokens WHERE token=?', (token,))
  token_info = token_info.fetchone()
  if not token_info:
    return (0.0, 0)
  # Time matters, in order to get latest/hottest news.
  gaussian_func = lambda x: (1 / math.sqrt(2 * math.pi * SIGMA)) * math.exp(-(x) ** 2 / (2 * SIGMA ** 2))
  str_to_datetime = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timestamp()
  time_now = datetime.now().timestamp()
  INTERVAL = 21600
  gaussian_para = (str_to_datetime(token_info[4]) - time_now) / INTERVAL
  gaussian_value = gaussian_func(gaussian_para)
  return ((token_info[0] * RATIO_ECON + token_info[1] + token_info[2] * RATIO_TITLE + token_info[2]) * gaussian_value,
          gaussian_value)


def query_text(text: str, is_title: bool, is_verge: bool) -> float:
  tokens = handle_text(text, is_title, is_verge)
  token_score = list(map(lambda x: query_token(x['value']), tokens))
  gaussian_para = sum([x[1] for x in token_score])
  if gaussian_para:
    token_score = sum([x[0] for x in token_score]) / gaussian_para
  else:
    token_score = 0
  token_score = (token_score * (RATIO_TITLE if is_title else 1) *
                 (1 if is_verge else RATIO_ECON))
  # token_score /= len(tokens)
  return int(token_score)


if __name__ == '__main__':
  all_posts = read_all_posts()
  run_all(all_posts)
  pass
