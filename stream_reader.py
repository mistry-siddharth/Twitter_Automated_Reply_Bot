#Following file contains the Editorial Logic & Reply Logic
import json
from pprint import pprint
import PIL, textwrap
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import tweepy, time, sys, json, random, datetime
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


#enter the corresponding information from your Twitter application:
consumer_key = 'wrnJqh9eNG97DBZe7QFgFEELK' #keep the quotes, replace this with your consumer key
consumer_secret = 'Q30JdLsiv1xUJnuWBf7oKy3aJDbqrWw8CSqAhnPxWLBU2kXxW7'#keep the quotes, replace this with your consumer secret key
access_token = '3254298862-GUoTTNlqIzDEAhIK87ftwd0ez2tvANJCEnB4ZAA'#keep the quotes, replace this with your access token
access_token_secret = 'hUFQM9yzBxGrsSe8BrgmV5qje9imEWo5FyksBnIN8LVAz'#keep the quotes, replace this with your access token secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
api_count = 0

#This function takes the Tweet JSON as an input
#This module takes the Tweet JSON and then calls extract which will help in extracting the key requirements from it 
def tweet_reply(t,count):
	global api_count
	api_count = count		#We set the global api_count variable to the one sent from stream.py script
	print(t)
	tweets_data_path = 'out.txt'

	tweets_data = []
	tweets_file = open(tweets_data_path, "r")
	for line in tweets_file:
		#print(line)
		try:
			tweet = json.loads(line)
			tweets_data.append(tweet)
		except:
			continue
	print("Will call extract")
	tweet_data = tweets_data[0]
	print(tweet_data)
	extract(t,tweet_data)
	print("----------------------")
	return api_count

#this is an optional module. It opens the wikipedia event facts and returns a fact from the threshold defined below
def fact_from_same_decade():
	factList = []
	with open('scrape.txt') as f:
		lines = f.readlines()
		year = 1945		#median year
		lower_limit = year-10	#makes sure facts start from 1935
		upper_limit = year+10	#makes sure facts end before 1945
		for line in lines:
			#year_int = int(line[0:4])
			year_int = year_int_converter(line)
			#if year_int>=lower_limit and year_int<=upper_limit:
			factList.append(line)
				#count = count+1				
				#print("Line:"+line)
	if len(factList) > 0:
		random_fact = randomLine(factList)
	else:
		random_fact = None
	return random_fact

#This is a sub function which converts a string year to int based which can be used for computation
def year_int_converter(tweet):
	s = ""
	for i in tweet:
		if i==" ":
			break
		s = s+i
	return int(s)

#this is a helper function used for prining the factlist... It is used for debugging
def pList(factList):
	for val in factList:
		print(val)

#This function returns a RANDOM fact from the scrape.txt file
def randomLine(factList):
	return random.choice(factList)

#This subfilter further allows to focus on the tweet content. Here, if below keyword are present in the Tweet 'message'
#Then only will it reply to the user or else it will skip the tweet. 
#This is useful for targetting particular patterns... So you filter all tweets with certain hashtag & then futher filter on keyword set in message
def subfilter(msg):
	print("In subfilter")
	print(msg)
	# TODO: bug in checking if key is in msg
	keyword_set = ["riot","riots","demonstration","demonstrations","march","rally","revolt"]
	for key in keyword_set:
		if key in msg.lower():
			print(msg)	
			return True
		else:
			print("Subfilter miss!!")
	return False
		
	
#This function takes in the tweet and the tweet information as input. It then further calls message which will package items (reply module)
def extract(t,tweet_data):
	user = tweet_data['user']['screen_name']
	tweet = tweet_data['text']
	tweet_id = tweet_data['id']
	print("user:"+user+" "+str(tweet_id))
	if subfilter(tweet):
		message(t,user,tweet_id)
	else:
		message(t,user,tweet_id)
	return		

def check_api_limit():
	global api_count
	api_count = api_count + 1
	return True
	

#===============Image Module=======================
#Since Twitter allows only 140 character limit, we convert the fact to an image. Below modules allow you to do that

#This module allows wrapping the text so that is can be converted to an image properly
def wrap_text(wrap,font,draw):
	margin = offset = 20
	margin = 20
	for line in wrap:
		draw.text((margin,offset),line,font=font,fill="#333333")
		offset += font.getsize(line)[1]

#This module takes in the message and converts it to an image. It has internal helper module which help in 
def create_image(message):
	wrap = textwrap.wrap(message,width=50)
	print(wrap)
	font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf",15)
	img=Image.new("RGBA", (450,40+18*len(wrap)),(255,255,255))
	draw = ImageDraw.Draw(img)
	#draw.text((10, 10),message,(0,0,0),font=font)
	wrap_text(wrap,font,draw)
	draw = ImageDraw.Draw(img)
	draw = ImageDraw.Draw(img)
	img.save("tweet_reply.png")
#=============Image Module ends====================

#This function gets the current year
def get_year(message):
	s = ""
	for char in message:
		if char != " ":
			s=s+char
		else:
			break
	return s

#This function cooks the wikipedia link to be sent as a source in Tweet Reply
def wikipedia_link():
	i = datetime.datetime.now()
	month = i.month
	day = str(i.day)
	months = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
	curr_month = months[month]
	link = "http://en.wikipedia.org/wiki/"+curr_month+"_"+day
	print("--------DEBUG/WIKI------")
	print(link)
	return link

#This function helps in tweeting back a reply. This is where the main message is cooked along with the calls to different child function to help build it
def message(t,user,tweet_id):
	f = fact_from_same_decade()

	# If there are no facts for today then don't tweet
	if f == None:
		return

	#print("In messages:"+t)
	#api.update_status(status=msg,in_reply_to_status_id=tweet_id)
	uni = unicode(f,"utf-8")
	create_image(uni)
	year = get_year(uni)
	link = wikipedia_link()
	print("--------DEBUG------")
	print(year)
	print("--------DEBUG------")
	at = ".@"+user
	#at =""
	status = at+" "+"But did you also know that on #ThisDayInHistory in "+year+" "+link
	image = "tweet_reply.png"
	reply(image,status,tweet_id)
	#tall_tweet(f,tweet_id)
	return

#This is the reply module... This gets the message as input and using Twitter API to reply the message
def reply(image,status,reply_id):
	probability = 1
	rand = random.random()
	print("Probability value generated: "+str(rand))
	if rand<=probability:
		api_limit_check_flag = check_api_limit()
		if api_limit_check_flag:	#only if all the parameters are fulfilled, we call the API limiter to increment the API_count 
			print("###################################################################")
			api.update_with_media(filename=image,status=status,in_reply_to_status_id=reply_id)	

#This is an optional function which allows breaking of tweet into 140 characters so that it can fit in a reply
def tall_tweet(tweet,tweet_id):
	n = len(tweet)
	if n > 140:
		n_tweet = n/125+1
		lower = 0
		higher = 125
		for i in range(0,n_tweet):
			s = tweet[lower:higher]
			if i==0:
				m = str((i+1))+"/"+str(n_tweet)+" "+s+"..."
				api.update_status(status=m,in_reply_to_status_id=tweet_id)		
			elif i<n_tweet-1:
				m= str((i+1))+"/"+str(n_tweet)+" "+"..."+s+"..."
				api.update_status(status=m,in_reply_to_status_id=tweet_id)
			else:
				m = str((i+1))+"/"+str(n_tweet)+" "+"..."+s
				api.update_status(status=m,in_reply_to_status_id=tweet_id)				
			lower = higher					
			higher = higher+125
	else:
		api.update_status(status=tweet,in_reply_to_status_id=tweet_id)

#This is an extra function to print tweet data used for debugging
def do_print():
	tweets_data_path = 'out.txt'
	tweets_data = []
	tweets_file = open(tweets_data_path, "r")
	for line in tweets_file:
		#print(line)
		try:
			tweet = json.loads(line)
			tweets_data.append(tweet)
		except:
			continue
#print tweets_data[0]['text']
	for tweet in tweets_data:
		print("Tweet-> ")
		print(tweet['text'])
		print(tweet['user']['name'])
	print("----------------------")
