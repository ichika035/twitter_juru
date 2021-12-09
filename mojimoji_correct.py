KEYS = {
'access_token' :'自分のやつ書いてね',
'access_token_secret':'自分のやつ書いてね',
'api_key' :'自分のやつ書いてね',
'api_secret' : '自分のやつ書いてね'

}

#correct Twitter data
import json
from requests_oauthlib import  OAuth1Session
twitter = OAuth1Session(KEYS['api_key'],KEYS['api_secret'],KEYS['access_token'],KEYS['access_token_secret'])

def getTwitterData(key_word,latitude,longtitude,radius,repeat=10):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    #取得パラメータ
    params = {'q':key_word,'count':'100','geocode':'%s,%s,%skm' % (latitude,longtitude,radius),'result_type':'recent'}
    tweets = []
    mid = -1

    for i in range(repeat):
        params['max_id'] = mid #midより古いIDをツイート
        res = twitter.get(url,params = params)
        if res.status_code ==200:
            #レスポンスからツイートする
            sub_tweets = json.loads(res.text)['statuses']

            user_ids = []

            for tweet in sub_tweets:
                user_ids.append(int(tweet['id']))
                tweets.append(tweet)

            if len(user_ids)>0:
                min_user_id = min(user_ids)
                mid = min_user_id -1
            else:
                mid = -1
                print(mid)
        else:
                print("Failed:%d" % res.status_code)

    print("ツイート取得数:%s" % len(tweets))
    return tweets

import time,calendar

def YmdHMS(created_at):
    time_utc = time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime("%Y/%m¥/%d %H:%M:%S",time_local)

#latitude35.1686111111 longtitude:136.910277778

tweets_atuma = getTwitterData("サイトウ",35.1761591,136.9082679,20,repeat=10)
for tweet in tweets_atuma:
    print(YmdHMS(tweet["created_at"]))
    print(tweet["text"]+"\n")
