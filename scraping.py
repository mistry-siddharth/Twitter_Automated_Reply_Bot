import bs4, requests, re, random
import string

#This function gets a single event text as input and it checks if the text sent contains any of the words mentioned below
#If present, it return the text or else it returns None
#In Order to add in more keywords, please add it here in the array
def check_keyword(text):
	keyword_set = ["riot","riots","demonstration","demonstrations","rally","revolt","revolution","coup","protest"]
	punctuations = string.punctuation # includes following characters: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
	for p in punctuations:
	    text = text.replace(p, "") 

	text_tokens = text.lower().split(" ")
	
	for key in keyword_set:
		if key in text_tokens:
			print(key)
			print(text)	
			return text

#This recieves a single even text as input and sends it to check_keyword to find if the fact contains protest related keywords
#Will return True if it does and False if it doesn't
def filter_facts_by_keyword(text):
	match_line = check_keyword(text)
	if match_line != None:
		return True
	else:
		return False
	
#The below function scrapes facts from Wikipedia for the current day.
#It takes the month and day as inputs and opens the wikipedia pages and scrapes all facts
#It makes sure the facts have particular keywords mentioned in the check_keyword function
#It outputs the facts in a text file named 'scrape.txt'
def scrape_wiki(month,day):
	str = "http://en.wikipedia.org/wiki/"+month+"_"+day	#This cooks the string which will be a GET api call
	response = requests.get(str)			
	soup = bs4.BeautifulSoup(response.text, "html.parser")			#BS4 allows scraping of text from HTML
	div_toc = soup.find("div",{"id":"toc"})			
	ul = div_toc.findNextSibling('ul')
	all_li = ul.find_all('li')				#It finds the div of the events

	myfile = open('scrape.txt','w')
	for item in all_li:
		text = item.getText()
		if len(text)<600:				#It only gets facts that are less than 600 characters
			if filter_facts_by_keyword(text):
				myfile.write(text.replace("\n","").encode('utf-8')+"\n")
	#print(all_li)
	myfile.close()


#Below is dummy unit test for code
#scrape("april","18")
#scrape_wiki("June","6")
#fact_from_same_decade()
