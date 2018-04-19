# -*- coding: utf-8 -*-
 
import tweepy, time, sys, json
 
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

status_reply = "WARNING! This post has been made by an impostor attempting to run a scam! Please continue accordingly. #CryptoScamDetector"

account_list = ['vergecurrency']

def updateScammerStatus(name):
	post = "@"+name+" has been detected to be an impostor!"
	update = api.update_status()

def reportSpam(id):
	report = api.report_spam(user_id=id)
	print(id, " has been reported!")



def getUserID(accounts):
	list_id = []
	for target in account_list:
		user = api.get_user(target)
		list_id.append(user.id)
	return list_id

def getTweetId(accounts):
	list_id = []
	for item in account_list:
		alltweets = api.user_timeline(screen_name =item, count = 1)
		for tweet in alltweets:
			list_id.append(tweet.id)
	return list_id

def getReplies(name):
	replies=[] 
	non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	post_tag_name = api.get_user(name)
	tag_parsed = json.dumps(post_tag_name._json)
	post_tag_name = json.loads(tag_parsed)
	post_name = post_tag_name['name']
	for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=name,timeout=999999).items(10):
		for tweet in tweepy.Cursor(api.search,q='to:'+name,result_type='recent',timeout=999999).items(200):
			if hasattr(tweet, 'in_reply_to_status_id_str'):
				if(tweet.in_reply_to_status_id_str==full_tweets.id_str):
					replies.append(tweet.id)
		for element in replies:
			stat = api.get_status(id=element)
			parsed = json.dumps(stat._json)
			parsed = json.loads(parsed)
			screen_name = parsed['user']['screen_name']
			user_name = parsed['user']['name']
			if(user_name == post_name):
				if(screen_name != name):
					print("Impostor!")
					print(screen_name)
					print(user_name)
					id = parsed['user']['id']
					print(parsed['user']['id'])
					reportSpam(id=id)
					status = api.update_status(status_reply, in_reply_to_status_id=element)
					updateScammerStatus(name=user_name)
		replies.clear()

id_list = getUserID(accounts = account_list)
tweet_id = getTweetId(accounts = account_list)

for account in account_list:
	getReplies(name=account)
	print("Sleeping...")
	time.sleep(400)
