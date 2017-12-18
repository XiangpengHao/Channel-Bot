import pymysql
from config import MYSQL_CONFIG


class Connection():
  def __init__(self, db_name='iot_data'):
    self._db_name = db_name
    self._table_name = 'channel'
    self._connection = self._get_connection()
    self._cursor = self._connection.cursor()
  
  def _get_connection(self) -> pymysql.cursors:
    mysql_conn = pymysql.connect(
      host=MYSQL_CONFIG['host_name'],
      user=MYSQL_CONFIG['user'],
      password=MYSQL_CONFIG['password'],
      port=MYSQL_CONFIG['server_port'],
      db=self._db_name,
      charset='utf8'
    )
    return mysql_conn
  
  def add_message(self, message_id: int, date: int, text: str, channel_name: str):
    sql = 'insert into {table_name}(date,text,chanelname,message_id) values(%s,%s,%s,%s)'.format(
      table_name=self._table_name)
    self._cursor.execute(sql, (date, text, channel_name, message_id))
    self._connection.commit()
  
  @property
  def cursor(self) -> pymysql.cursors:
    return self._cursor
  
  def close(self):
    self._connection.close()
  
  def commit(self):
    self._connection.commit()
  
  def commit_and_close(self):
    self.commit()
    self.close()
