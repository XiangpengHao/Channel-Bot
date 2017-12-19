import json, requests, random
from config import NEWS_SOURCES
import os

DEBUG = 'BOT_DEBUG' in os.environ


class NewsProvider():
  def __init__(self, sources=NEWS_SOURCES):
    self.sources = sources
    self.post_list = {}
    pass
  
  def _get_posts(self):
    if DEBUG:
      import sample_rv
      self.post_list = sample_rv.rv
      return self.post_list
    for source, url in self.sources.items():
      result = requests.get(url).content.decode()
      result_json = json.loads(result)
      self.post_list[source] = result_json['articles']
    return self.post_list
  
  def _format_all(self) -> dict:
    important = self.post_list['important']
    unimportant = self.post_list['unimportant']
    
    important = [self._format_important(a) for a in important]
    unimportant = [self._format_unimportant(a) for a in unimportant]
    
    prev_source = unimportant[0][0]
    unimportant_text = '*{source}* --------------------\n\n'.format(source=prev_source)
    for index, item in enumerate(unimportant):
      if item[0] != prev_source:
        unimportant_text += '*{source}* --------------------\n\n'.format(source=item[0])
        prev_source = item[0]
      unimportant_text += '*{index}*. {item}\n'.format(index=index + 1, item=item[1])
    return {'important': important, 'unimportant': [unimportant_text]}
  
  def _format_important(self, article: dict) -> str:
    return '[{title}]({url})'.format(title=article['title'], url=article['url'])
  
  def _format_unimportant(self, article: dict) -> tuple:
    return (article['source'], '({importance}) [{title}]({url})\n'.format(
      source=article['source'], importance=article['importance'],
      title=article['title'], url=article['url']
    ))
  
  def _classify(self) -> dict:
    important = []
    unimportant = []
    for source, articles in self.post_list.items():
      for article in articles:
        importance = self.check_importance(
          article['title'], article['description'], source
        )
        article['source'] = source
        article['importance'] = importance
        if importance > 85:
          important.append(article)
        elif importance > 15:
          unimportant.append(article)
    self.post_list = {'important': important, 'unimportant': unimportant}
    return self.post_list
  
  @staticmethod
  def check_importance(title: str, desc: str, source: str) -> int:
    return random.randrange(0, 100)
  
  def get_send_message(self) -> dict:
    self._get_posts()
    self._classify()
    rv = self._format_all()
    return rv
