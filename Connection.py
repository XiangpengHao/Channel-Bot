import pymysql
from config import MYSQL_CONFIG
import datetime
from typing import List


class ConnectionBase():
  def __init__(self, db_name='iot_data', table_name='channel'):
    self._db_name: str = db_name
    self._table_name: str = table_name
    self._connection = self._get_connection()
    self._cursor: pymysql.cursors.Cursor = self._connection.cursor()
  
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    self._connection.close()
  
  def _get_connection(self):
    mysql_conn = pymysql.connect(
      host=MYSQL_CONFIG['host_name'],
      user=MYSQL_CONFIG['user'],
      password=MYSQL_CONFIG['password'],
      port=int(MYSQL_CONFIG['server_port']),
      db=self._db_name,
      charset='utf8'
    )
    return mysql_conn
  
  @property
  def cursor(self) -> pymysql.cursors.Cursor:
    return self._cursor
  
  def close(self):
    self._connection.close()
  
  def commit(self):
    self._connection.commit()
  
  def commit_and_close(self):
    self.commit()
    self.close()


class ConnectionNews(ConnectionBase):
  def __init__(self, table_name='news'):
    ConnectionBase.__init__(self, 'iot_data', table_name)
  
  def insert_news(self, author: str, title: str, description: str, url: str, published_at: str, source: str,
                  importance: int):
    sql = 'INSERT INTO {table_name}(author,title,description,url,`date`,`source`,`importance`) VALUES(%s,%s,%s,%s,%s,%s,%s)'.format(
      table_name=self._table_name
    )
    self.cursor.execute(sql, (author, title, description, url, published_at, source, importance))
    self.commit()
  
  def check_existence(self, url: str):
    sql: str = 'SELECT exists(SELECT `url` FROM `news` WHERE `url`=%s LIMIT 1)'
    self.cursor.execute(sql, (url,))
    item_exist = self.cursor.fetchone()
    return int(item_exist[0])


class ConnectionChannel(ConnectionBase):
  def __init__(self, table_name='channel'):
    ConnectionBase.__init__(self, 'iot_data', table_name)
  
  def insert_message(self, message_id: int, date: datetime.datetime, text: str, channel_name: str):
    sql = 'insert into {table_name}(date,text,channel_name,message_id) values(%s,%s,%s,%s)'.format(
      table_name=self._table_name)
    self._cursor.execute(sql, (date, text, channel_name, message_id))
    self.commit()
  
  def mark_delete(self, message_id: int, channel_name: str):
    sql = 'update {table_name} set deleted=1 where `message_id`=%s and `channel_name`=%s'.format(
      table_name=self._table_name)
    self._cursor.execute(sql, (message_id, channel_name))
    self.commit()
  
  def get_yesterday_not_deleted(self, channel_name: str) -> List:
    sql = 'select message_id from {table_name} where deleted=0 and `channel_name`=%s and `date` between subdate(current_date,1) and subdate(current_date,0)'.format(
      table_name=self._table_name
    )
    self._cursor.execute(sql, (channel_name,))
    ids = self.cursor.fetchall()
    return [int(a[0]) for a in ids]
