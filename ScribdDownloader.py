#Scribd Downloader
#Adam Knuckey September 2015

print ("Starting Scribd Downloader")
import os
import re
import urllib, urllib2
import threading
from time import sleep

def download(link,destination):
	#print link
	urllib.urlretrieve(link,destination)

print("Enter textbook link:")
website = raw_input(" > ")
request = urllib2.Request(website)
request.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
opener = urllib2.build_opener()
html = opener.open(request).read()
regex = re.compile("<title>.+</title>")
for m in regex.finditer(html):
	title = m.group().replace("<title>","").replace("</title>","")

print ("Download "+title+"?")
proceed = raw_input("(y/n) > ").lower()

if proceed == "y":
	print ("Downloading textbook - "+title+"...")
	index = html.index('pageParams.contentUrl = "https://html2-f.scribdassets.com/')+len('pageParams.contentUrl = "https://html2-f.scribdassets.com/')
	ident = html[index:index+17]

	if not os.path.exists(title):
	    os.makedirs(title)

	page = 1
	regex = re.compile(ident)
	for m in regex.finditer(html):#
		link = html[m.start()-len('https://html2-f.scribdassets.com/'):m.start()+23+len(str(page))+11].replace("pages","images")+".jpg"
		t = threading.Thread(target=download,args=(link,title+"/"+str(page)+".jpg"))
		t.daemon = True
		t.start()
		sleep(0.05)
		#print link
		#urllib.urlretrieve(link,title+"/"+str(page)+".jpg")
		page+=1
	print ("Downloaded "+str(page-1)+" pages")

else:
	print ("Exiting...")

