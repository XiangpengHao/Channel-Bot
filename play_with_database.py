from Models import *
from datetime import date
import datetime

db.connect()
try:
    db.create_tables([User, Content])
except Exception as error:
    print(error)
    exit()


def judge_if_spam_message(message):
    return False


def write_into_the_database(user_info, content_info):
    try:
        owned_user = User.create(user_name=user_info[0], user_id=user_info[1], is_relative=True)
        owned_user.save()
    except IntegrityError:
        owned_user = User.get(User.user_id == user_info[1])

    try:
        current_comment = Content.create(owner=owned_user,
                                         content=content_info,
                                         post_time=datetime.datetime.now,
                                         is_spam=judge_if_spam_message(content_info))
        current_comment.save()
    except Exception as e:
        print(e)
        return False
    return True


def retrive_from_database():
    pass
