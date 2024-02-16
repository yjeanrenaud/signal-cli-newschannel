#!/usr/bin/env python3
# based on https://www.reddit.com/r/raspberry_pi/comments/19pr93/using_my_raspberry_pi_to_monitor_an_rss_feed/ with unclear licence
# It gets the latest RSS feed entry and pushes it to all subscribers in the SQlite DB. 
# The subscriber db is filled by signal-cli-bot (https://github.com/yjeanrenaud/signal-cli-bot)
# 2020 Yves Jeanrenaud for PocketPC.ch 

print(".oO0 Passive PocketPC.ch News Pusher for signal-cli 0Oo.")

import os,sys
dbFilename= os.path.abspath(os.path.dirname(sys.argv[0]))+'/signal.db'

import os, sys
from requests import head, get, post
from time import sleep, struct_time # we won't need all time functions!
from feedparser import parse
from os import system
from pprint import pprint
import re
import urllib.request

def yj_send_signals (strNews):
	from pydbus import SystemBus
	import sqlite3
	
	# db file is there for sure
	# connect to db
	try:
		connection = sqlite3.connect(dbFilename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
	except Error as e:
		print(e)
	
	# create db cursor
	cursor = connection.cursor()
	# connect to signal-cli via dbus
	bus = SystemBus()
	signal = bus.get('org.asamk.Signal')
	# ask for the subscriber list
	sql = "SELECT phone FROM subscribers"
	cursor = connection.execute(sql)
	results = cursor.fetchall()
	if len(results)>1:
		#send to each subscriber
		for subscriber in results:
			signal.sendMessage(strNews, ['/tmp/signal-thumb.png'], ["\'"+str(subscriber[0])+"\'"])
			print("signal sent to "+str(subscriber[0]))
	else:
		# we have only one subscriber, so send only to that one
		signal.sendMessage(strNews, ['/tmp/signal-thumb.png'], ["\'"+str(results[0][0])+"\'"])
		print("signal sent to "+str(results[0][0]))
		
	print("all signals sent")
	return


if os.path.exists(dbFilename):
	print("Datenbank-Datei \""+dbFilename+"\" ist vorhanden")
else:
	print("Datenbank-Datei \""+dbFilename+"\" NICHT vorhanden!?")
	sys.exit()
	
import datetime
print(str(datetime.datetime.now()))
#init the sources' config
characters = head('https://www.pocketpc.ch/magazin/feed/').headers['content-length']
r = get('https://www.pocketpc.ch/magazin/feed/')
d = parse(r.content)
# oldID stores the current topmost entry's URL in the rss feed. When your feed has other unique identifiers, you may use them, too.
oldID = d.entries[0].link ##init value
print("init oldD="+oldID)
print(str(datetime.datetime.now()))
# welcome to the pit
print("now go and watch the feed, quietly...")
while 1:
	#we do not want to parse the feed every time nor download the feed every time we check for an update
	new_query = head('https://www.pocketpc.ch/magazin/feed/').headers['content-length']
	print ("new_query: "+str(new_query)+" | characters: "+str(characters) + " @ "+ str(datetime.datetime.now()))
	if new_query == characters:
		#nothing changed, the number of characters is the same
		#so wait a minute
		sleep(60)
	else:
		print("something changed!" + str(datetime.datetime.now()))
		#actually it is fewer or more characters in the rss, which is an indicator for change due to we miss all the meta data in our feed header
		characters = new_query
		#now preprate to read the latest entry
		r = get('https://www.pocketpc.ch/magazin/feed/')
		d = parse(r.content)
		#topmost entry is enough for us
		#so first, verify we did not push that yet due to erroreous updates, dst shifts etc.
		print ("d.entries[0].link: "+ d.entries[0].link+" | oldID: "+oldID)
		print(str(datetime.datetime.now()))
		if d.entries[0].link != oldID:
			#ok, now go and set the ID to check for next
			oldID = d.entries[0].link
			#prepare the news for broadcast as a string
			strNews=d.entries[0].title +"\n"+ d.entries[0].link
			print("NEWS\n###\n"+strNews+"\nid="+d.entries[0].id+"\n")
			print(str(datetime.datetime.now())+"...")
			#get the thumbnail image
                        regex = r"src=\"([a-zA-Z0-9:/?\.\-]*)\""
                        test_str=(d.entries[0].description)
                        matches = re.search(regex, test_str, re.MULTILINE)
                        urllib.request.urlretrieve(matches[1],"/tmp/signal-thumb.png") #because matches[0] is the whole match, not the group
			#attachments need to be files anyway, so we don't send it to the function
			yj_send_signals(strNews) #now broadcast!

		else:
			print("no NEWS today\noldID=newID="+oldID)
			print(str(datetime.datetime.now())+"...")
		sleep(1200) #because the mid night cronjob messes with the feed entry order on pocketpc.ch
