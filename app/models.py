# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


# 管理员工号
class User(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


# 通知人配置
class CfgNotify(BaseModel):
    check_order = IntegerField()  # 排序
    notify_type = CharField()  # 通知类型：MAIL/SMS
    notify_name = CharField()  # 通知人姓名
    notify_number = CharField()  # 通知号码
    status = BooleanField(default=True)  # 生效失效标识

#推文配置
class Tweet(BaseModel):
    tweet_id=CharField()
    tweet_user_id=CharField()
    tweet_user_name=CharField()
    tweet_user_nick = CharField()
    retweet_id = CharField()
    retweet_user_name = CharField()
    retweet_user_nick = CharField()
    tweets = CharField()
    ex_url = CharField()
    url_title = CharField()
    url = CharField()
    hashtags = CharField()
    ex_media_url = CharField() #原始推文url
    media_url = CharField() #短网址原始推文url
    user_mentions_name = CharField()
    user_mentions_nick = CharField()
    tweet_user_name = CharField()
    time=CharField()


#推特用户配置
class Twitter(BaseModel):
    user_name = CharField()
    user_nick = CharField()
    recent_active_time=CharField()
    number_of_tweets=CharField()
    user_mentions_name=CharField()
    hashtags=CharField()
    exurl=CharField()



@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


# 建表
def create_table():
    db.connect()
    db.create_tables([CfgNotify, User])


if __name__ == '__main__':
    create_table()
