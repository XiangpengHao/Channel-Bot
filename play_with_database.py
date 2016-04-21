from Models import *
from datetime import date
import datetime

'''
try:
    db.create_tables([User, Content])
except Exception as error:
    print(error)
    exit()
'''


def judge_if_spam_message(message):
    return False


def check_database():
    db.connect()
    try:
        db.create_tables([User, Content])
    except Exception as error:
        print(error)


def write_into_the_database(user_info, content_info):
    check_database()
    try:
        owned_user = User.create(user_name=user_info[0], user_id=user_info[1], is_relative=True)
        owned_user.save()
    except IntegrityError:
        owned_user = User.get(User.user_id == user_info[1])

    try:
        current_comment = Content.create(owner=owned_user,
                                         content=content_info,
                                         is_spam=judge_if_spam_message(content_info))
        current_comment.save()
    except Exception as e:
        print(e)
        return False
    return True


def retrive_from_database():
    all_data_list = []
    for content in Content.select():
        all_data_list.append(content.content)
    return all_data_list


def statistic_today():
    today_telegram_content = Content.select().where(
       Content.post_time.day == datetime.datetime.now().day)
    # today_telegram_content = Content.select().where(
    #     Content.post_time.day == 20)
    total_dict = {}
    for each_content in today_telegram_content:
        user_name = each_content.owner.user_name
        if user_name not in total_dict:
            total_dict[each_content.owner.user_name] = 1
        else:
            total_dict[each_content.owner.user_name] += 1

    result_string = "Today's statistics: \n**************\n"
    for content_owner, owner_frequency in total_dict.items():
        result_string += '%s:    %s\n' % (content_owner, owner_frequency)
    return result_string[:-1]
