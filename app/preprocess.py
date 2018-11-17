# -*- coding: utf-8 -*-
import pymysql.cursors
import time

def getInfoByUserName(connection,name):
    #返回关于user的字典,通过名字查找获得
    result = None
    with connection.cursor() as cursor:
        sql = 'select user_mentions_name, ex_url, hashtags, time FROM t_tweets WHERE tweet_user_name = %s'
        cursor.execute(sql,(name,))
        user = cursor.fetchall()#相当于一个拥有行数数量的字典组成的元组
        result = washInfo(user)#获得插入时要用到的数据,字典形式
    return result
        
def washInfo(user):
    #存储从数据库中的到的数据
    mentions = []
    ex_urls = []
    tags = []
    times = []
    result = {}
    for row in user:
        mentions.extend(row['user_mentions_name'].split(','))
        ex_urls.extend(row['ex_url'].split(','))
        tags.extend(row['hashtags'].split(','))
        times.append(row['time'])
        
    result['recent_active_time'] = getRecentTime(times)
    result['exurl'] = getExurl(ex_urls)
    result['hashtags'] = getTags(tags)
    result['user_mentions_name'] = getUserMentionsName(mentions)
    return result
        
#帮助比较时间
def getTimeStamp(ori_time):
    format_time = ori_time[:20] + ori_time[-4:]
    time_stamp = time.mktime(time.strptime(format_time,"%a %b %d %H:%M:%S %Y"))
    return time_stamp

#传入列表获得最近时间
def getRecentTime(time_list):
    result = time_list[0]
    result_stp = getTimeStamp(result)
    for time in time_list:
        tmp = getTimeStamp(time)
        if tmp > result_stp:
            result = time
    return result


#传入tags列表，统计并排序返回列表前五
def getTags(tags):
    freq = {}
    #去None
    while '' in tags:
        tags.remove('')
        
    set_tags = set(tags)
    for tag in set_tags:
        freq[tag] = tags.count(tag)
    sort_tags = sorted(freq.items(),key=lambda freq:freq[1], reverse=True)
    #获得前五的标签
    result = sort_tags[:5]
    result = joinTags(result)
    return result
    
#传入tag对的元组的列表，合成一个字符串
def joinTags(tags):
    result = []
    for tag_pair in tags:
        tag = tag_pair[0] + '(' + str(tag_pair[1]) + ')'
        result.append(tag)
    result = ";".join(result)
    return result

#把url合并
def getExurl(ex_urls):
    while '' in ex_urls:
        ex_urls.remove('')
    result = set(ex_urls)
    result = ";".join(result)
    return result

#获得mentionsname
def getUserMentionsName(mentions_names):
    freq = {}
    #去None
    while '' in mentions_names:
        mentions_names.remove('')
    #去重
    set_mentions = set(mentions_names)
    for mention in set_mentions:
        freq[mention] = mentions_names.count(mention)
    #排序
    sort_mentions = sorted(freq.items(),key=lambda freq:freq[1], reverse=True)
    #获得前五的@人
    result = sort_mentions[:5]
    result = joinMentions(result)
    return result

def joinMentions(mentions):
    result = []
    for name_pair in mentions:
        name = name_pair[0] + '(' + str(name_pair[1]) + ')'
        result.append(name)
    result = ";".join(result)
    return result

if __name__ == '__main__':
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='toor',
                             db='flaskdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            #用来获取不重复的用户name,nick
            sql = "select `tweet_user_name`,`tweet_user_nick`,COUNT(id) from t_tweets group by tweet_user_id"
            insert = "INSERT  INTO  twitter (`user_name`, `user_nick`,`recent_active_time`,`number_of_tweets`,`user_mentions_name`,`exurl`,`hashtags`) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            update = connection.cursor()#用于提交

            cursor.execute(sql)

            
            #tweet (username nick)
            row = cursor.fetchone()
            while not row is None:
                print(row)
                name = row['tweet_user_name']
                nick = row['tweet_user_nick']
                number_of_t = row['COUNT(id)']

                record = getInfoByUserName(connection,name)

                user_mentions_name = record['user_mentions_name']
                exurl = record['exurl']
                hashtags = record['hashtags']
                active_time = record['recent_active_time']

                #这个操作没写完
                update.execute(insert,(name,nick,active_time,number_of_t,user_mentions_name,exurl,hashtags))
                connection.commit()
                row = cursor.fetchone()
    finally:
        pass
