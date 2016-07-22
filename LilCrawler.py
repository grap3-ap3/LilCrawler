#!/usr/bin/python
#Author: Phil Grimes @grap3_ap3	
#Python 2.7.1 (r271:86832, Apr 12 2011, 16:15:16) 
#[GCC 4.6.0 20110331 (Red Hat 4.6.0-2)] on linux2
#Date: 2011-12-26 19:47:04 
#Revision: 1.0
#Description: This is a simple web crawler. Give it a target and decide how deep to dig, it will give you a text file of the found links.

#Here we impore the modules we need
import urlparse
import urllib
import httplib
import sys
import re
import argparse
import time
from urllib2 import urlopen

#<Definitions>
#Our variables
url = raw_input("Enter Target URL: ")
depth = input("Enter desired depth: ") # recursion depth max
master_db = {}
node = [url]
outputFile = 'foundTheseLinks.txt'


#This function handles saving the results.
def saveToDisk(outputFile, master_db):
	file = open(outputFile, 'a')
	for key,values in master_db.iteritems():
		file.write("%s\n" % key)
		for item in values:
			file.write("\t%s\n" % item)
	file.close

#This function checks the link to see if it's alive.
def checkLinkLife(thisLink, path="/"):
    try:
        conn = httplib.HTTPConnection(thisLink)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except(StandardError):
        #print 'Link Exception Found!: ',thisLink
		return()

#This function validates the links we find as we dig
def validate(thisLink):
	thisLink = urlparse.urlparse(thisLink)
	if thisLink.scheme == '':
		thisLink = thisLink.path
	else:
		thisLink = thisLink.netloc
	try:
 		linkLife =  checkLinkLife(thisLink)
		if linkLife == 200:
			print 'We got a live one! ',thisLink
			return thisLink
		else:
			print 'Dead Link: ',thisLink
			context_node.remove(thisLink)
	except:
		#print 'VALIDATION EXCEPTION',thisLink
		return()


#This function does the actual work.
def crawl(thisLink):
	links_found = 0
	thisLink = urlparse.urlparse(thisLink)
	string = 'http://'
	if thisLink.scheme == '':
		newUrl = string+thisLink[1]+thisLink[2]
	else:
		newUrl = thisLink[0]+'://'+thisLink[1]+thisLink[2]
	try:
		crawlUrl = urllib.urlopen(newUrl)
		crawledHtml = crawlUrl.readlines()
		crawledLinksFound = []
		crawledLink = re.compile(r'[a-zA-Z0-9\-\.]+\.[a-zA-Z]{1,4}')
		for line in crawledHtml:
			if len(line) != 0:
				crawledLinksFound.extend(crawledLink.findall(line))
		crawledLinksFound = list(set(crawledLinksFound))
		for link in crawledLinksFound:
			print(link)
			return crawledLinksFound
	except (IOError,TypeError):
		#print 'CRAWLING EXCEPTION: ',newUrl
		return()

#This is the main function that determines what the program will "do".
def main(url,node,depth,outputFile,master_db):
	print 'Target is ',url
	print 'max depth= ',depth
	print 'Saving results to ',outputFile
	for depth in xrange(depth):
		print "*"*70+("\nScanning depth %d web\n" % (depth+1))+"*"*70
		context_node = node
		node = []
		db = {}
		for thisLink in context_node:
			try:
				thisLink = validate(thisLink)
				theBounty = crawl(thisLink)
				theBounty = list(set(theBounty))
				for item in theBounty:
					node.append(item)
					db = {thisLink: theBounty}
					master_db.update(db)
			except(AttributeError,TypeError):
				#print 'Error',thisLink
				return()
	saveToDisk(outputFile, master_db)
#</Definitions>

#This is the loop that calls main.
if __name__ == "__main__":
	main(url,node,depth,outputFile,master_db)