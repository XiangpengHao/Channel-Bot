from peewee import *
import datetime

db = SqliteDatabase('../chat_log.db')


class User(Model):
    user_name = CharField()
    user_id = CharField()
    is_relative = BooleanField()

    def __str__(self):
        return self.user_name

    class Meta:
        database = db


class Content(Model):
    owner = ForeignKeyField(User, related_name='content')
    content = CharField()
    post_time = DateTimeField(default=datetime.datetime.now)
    is_spam = BooleanField()

    def __str__(self):
        return self.content

    class Meta:
        database = db
