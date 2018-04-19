# -*- coding: utf-8 -*-
 
import tweepy, time, sys, json
 
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

status_reply = "WARNING! This post has been made by an impostor attempting to run a scam! Please continue accordingly. #CryptoScamDetector"

account_list = ['vergecurrency']
blacklist = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    IMPOSTOR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def updateScammerStatus(name):
	post = "@"+name+" has been detected to be an impostor! #CryptoScamDetector"
	update = api.update_status(status=post)

def reportSpam(id):
	report = api.report_spam(user_id=id)
	print(id,"has been reported!")

def replyPost(id, name):
	status= "@"+name+" WARNING! This post has been detected to be a scam and has been thusly reported. #CryptoScamAlert"
	reply = api.update_status(status,id)


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
		print("Fetching Replies")
		for tweet in tweepy.Cursor(api.search,q='to:'+name,result_type='recent',timeout=999999).items(100):
			if hasattr(tweet, 'in_reply_to_status_id_str'):
				if(tweet.in_reply_to_status_id_str==full_tweets.id_str):
					replies.append(tweet.id)
		for element in replies:
			blacklist_flag = False
			stat = api.get_status(id=element)
			parsed = json.dumps(stat._json)
			parsed = json.loads(parsed)
			screen_name = parsed['user']['screen_name']
			user_name = parsed['user']['name']
			for b in blacklist:
				if(b == element):
					blacklist_flag = True
			if(blacklist_flag == False):
				if(user_name == post_name):
					if(screen_name != name):
						print(bcolors.IMPOSTOR + "Impostor detected!" + bcolors.ENDC)
						print(screen_name, user_name)
						id = parsed['user']['id']
						replyPost(id=element, name=screen_name)
						reportSpam(id=id)
						f = open("imposter_list.txt", "a+")
						f.write("Username: %s\n" % user_name)
						f.write("Screen name: %s\n" % screen_name)
						f.write("User id: %s\n" % id)
						f.write("Offending Tweet Id: %d\n\n" % element)
						f.close()
						blacklist.append(element)

		replies.clear()


for account in account_list:
	print(bcolors.OKGREEN + "Running check for " + account + bcolors.ENDC)
	getReplies(name=account)
	print("Sleeping for 15 minutes...")
	time.sleep(900)


