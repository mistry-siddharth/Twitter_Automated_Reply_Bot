# Twitter_Automated_Reply_Bot
Software Dependancies

Python v 3.5.2
Tweepy (latest version)
VirtualEnv (latest version)
Beautiful Soup (latest version)
Pillow (latest version)

Instructions

Please add the above dependancies to make sure the project works. Also, make sure you have a valid Twitter API key & Google API key that is added in the code itself.

Steps to get the content from github

Clone the github directory from the link
(Optional) Create a vitrual env in a folder as it makes things easier to install
(Optional) Instructions on installing virtualenv and creating a virtual directory are given here
Install the aforementioned dependancies
Follow individual deployment steps mentioned below for each bot

This bot works on the conecept of information dissemination. The bot is configurable to listen to any keywords/#hashtags/user and will be able to reply with a random fact scraped from Wikipedia.

Workflow

Pre-Processor Module: Scraping.py script is the pre-processor script. It scrapes events from Wikipedia matching certain critera
Tweet Listerner Module: Stream.py script has the configuration for changing the listening parameter.
Editorial Logic Module: This is present in the stream_reader.py file. It houses logic of retrieving a random fact from the wikipedia scraped items.
Reply Module: stream_reader.py also contains the module which helps in replying. It has a Text-to-Image convertor which allows replying with facts that are greater than 140 characters thereby bypassing the Twitter limit

How to Run

Make sure all the dependancies are installed
Open terminal or cmd and navigate to the directory where you have stored historybot.py
Execute following command: python historybot.py
