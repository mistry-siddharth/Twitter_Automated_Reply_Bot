#Following module acts as a Tweet Listener Module
# main() gets called first followed be all functions and scripts internally

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import stream_reader, time, datetime, scraping, sys #stream_reader & scraping are scripts in the same folder
import json

#enter the corresponding information from your Twitter application:
consumer_key = 'wrnJqh9eNG97DBZe7QFgFEELK' #keep the quotes, replace this with your consumer key
consumer_secret = 'Q30JdLsiv1xUJnuWBf7oKy3aJDbqrWw8CSqAhnPxWLBU2kXxW7'#keep the quotes, replace this with your consumer secret key
access_token = '3254298862-GUoTTNlqIzDEAhIK87ftwd0ez2tvANJCEnB4ZAA'#keep the quotes, replace this with your access token
access_token_secret = 'hUFQM9yzBxGrsSe8BrgmV5qje9imEWo5FyksBnIN8LVAz'#keep the quotes, replace this with your access token secret

#This is a basic listener that just prints received tweets to stdout.

class StdOutListener(StreamListener):
	def __init__(self,tweet,api=None):
		super(StdOutListener, self).__init__()
		self.num_tweets = 0			#tweet counter
		self.tweet_reply = tweet		#tweets
		self.date = datetime.datetime.now().day
		self.api_count = 0
		self.old_time = time.time()
	#This method checks if the date has changed so it can scrape the next days fact from Wikipedia
	def check_day_change(self):
		print("pre invoked")
		current_date = datetime.datetime.now().day
		print(current_date)
		if self.date!=current_date:
			print("----------Date Changed!!!----------")
			self.date = current_date
			return False
		return 

	#If a Tweet matches the listener criteria, below function is invoked
	#It takes the Tweet data and calls the answer method
	def on_data(self, data):
		#print(data)
		print(self.tweet_reply)
		flag = self.check_day_change()
		if flag == False:
			return False	#if the day has changed, break the listener and recall pre-process scraping.py script to scrape new day data

		tweet_data = json.loads(data)
		print(tweet_data)
		user = tweet_data['user']['screen_name']
		user_mentions = tweet_data['entities']['user_mentions']
		user_mentions_list = []
		for u in user_mentions:
			user_mentions_list.append(u["screen_name"])
		# Make sure the bot never responds to itself, or to any tweet where it's mentioned
		if user == "ProtestBot" or "ProtestBot" in user_mentions_list:
			return True
		else:
			#print(self.pre())
			f = open('out.txt','a')	#writes tweet data into file
			f.write(data)
			f.close()
			self.num_tweets = self.num_tweets + 1
			if self.num_tweets < 12:		#this is a window of tweets gathered before calling the answer method. By default it is 1 (it is preferable to keep window 1 which means on every tweet emited that matches criteria we process)
				return True
			else:
				self.answer()
				f = open('out.txt','w')
				f.truncate
				f.close
				return True

#This is the API limit checker module which checks if we do not exceed 180 Tweets per 15 minutes as per Twitter API limits
	def api_limit_checker(self):
		if time.time() - self.old_time > 900:	#If we are outside a 15 min window
			print("outside 15 min interval")
			self.old_time = time.time()	#Reset the timer of window since new window started & Twitter limits refreshed
			self.api_count = 0	#Reset the api counter to 0 since new window started & Twitter limits refreshed
		else:
			print("within the 15 minute interval")
			if self.api_count > 140:	#We check if we exceed the Tweet limit of 140 in 15 minutes
				time.sleep(900 - (time.time() - self.old_time))	#We put the code to sleep for 15-x minutes where x is the current time - old time (when the window started)... So if within 6 minutes we tweet more than 140 times, then the script will halt for the next 15-6=9 minutes until a new window starts
				self.api_count = 0	#Since we have slept through the remainder, a new window has started and we reset the API Count as well
				self.old_time = time.time() #Similarly as above, we reset the timer as well since new window has started 
				


	#Answer method takes the tweet data and sends it to the stream_reader.py script which has the editorial logic

	def answer(self):
		self.api_limit_checker()	#we invoke the API limit checker code
		curr_api_count = stream_reader.tweet_reply(self.tweet_reply,self.api_count)		#calls scripts with Business & Reply logic... This returns the current API_COUNT
		#stream_reader.do_print()
		self.api_count = curr_api_count	#We assign our API count to this returned variable
		print(self.api_count)	
		print("^^^^^")
		self.num_tweets = 0					#counter reset
		return			
	def on_error(self, status):
		print(status)

def stream_filter():
	print("Siddharth")

#This method is the pre-processor invocation module. It will call the scraping.py script which scrapes wikipedia fact into a file
def preprocess():
	months = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
	now = datetime.datetime.now()
	#print(now.day)
	curr_month = months[now.month]
	curr_day = now.day
	tweet_reply = scraping.scrape_wiki(curr_month,str(curr_day))
	return tweet_reply			

#Main is called from the script historybot.py
#Main first calls preprocess function which creates a facts file of events
#It then generates a connection to the Twitter API using tweepy
#trackObj allows you to target different thing one wants to tag such as certain hashtags, keywords, users, location etc.

def main():
	preprocessed_data = preprocess()
	#print("This is the reply:"+tweet_reply)
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener(preprocessed_data)
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	trackObj = ['#ThisDayInHistory','thisdayinhistory'] #tracks the hashtags list
	try:
		stream.filter(track=trackObj)
	except:
		pass
	#print(stream)
	print("reaching end")
	return
main()	

# export PYTHONIOENCODING=utf-8
#  nohup python -u historybot.py > nohup.txt &
