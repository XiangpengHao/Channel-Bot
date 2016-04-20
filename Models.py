from peewee import *
import datetime
db = SqliteDatabase('chat_log.db')


class User(Model):
    user_name = CharField()
    user_id = CharField()
    is_relative = BooleanField()

    class Meta:
        database = db


class Content(Model):
    owner = ForeignKeyField(User, related_name='content')
    content = CharField()
    post_time = DateTimeField(default=datetime.datetime.now)
    is_spam = BooleanField()

    class Meta:
        database = db
