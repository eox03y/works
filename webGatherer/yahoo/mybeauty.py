#!/usr/bin/env python
# -*- coding: euc-kr -*-

import urllib
import urlparse
import httplib
import urllib2

import BeautifulSoup

#httplib.HTTPConnection.debuglevel = 1 

urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')


Topurl = ['/News_and_Media', '/Computers_and_Internet','/Recreation','/Business_and_Economy', '/entertainment', '/Education', '/Health', '/Society_and_Culture', '/Government', '/Arts', '/Science', '/Humanities__Social_Science', '/Regional', '/Reference']
#Topurl = ['/Arts']
urltable = {}	# 1: '/A/B'

#url2table = {}      # '/A/B' : 1
didlist = []

# Save this to Database
#Category = { 1 : [] }
Category = {}

def myLink():
	''' This is only thing what I can do '''

	#soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="euc-kr")

	CategoryNum = 1

	while True:
		if len(Topurl) == 0:
			break

		yahoo_url = 'http://kr.dir.yahoo.com'
		token = Topurl.pop()

		if didlist.count(token) == 0:
		#if urltable.get(CategoryNum) == None:
			didlist.append(token)

			urltable[CategoryNum] = token
			CategoryNum += 1
		else:
			pass


		url = yahoo_url + token
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)

		html = response.read()
		soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="euc-kr")

		fp = open('mywebsite.txt', 'a')
		fc = open('mycategory.txt', 'a')
		#heading = soup.dd
		#print heading.renderContents()

		pty = soup.prettify()

		
		tmp = pty.find('base href')
		if tmp == -1:
			print 'not exist base href'
			continue
		basehrefs = pty [ tmp : tmp + 256 ]

		try:
			basehref = basehrefs.split('"')[1] # current site's baseurl
			#print urltable
		except:
			fpp = open('errormybeauty.log', 'a')
			print '____basehref_error_____'
			print 'token:', token
			#print pty
			print 'basehrefs:', basehrefs
			fpp.write(basehrefs + '\n')
			fpp.write(pty + '\n')	# current error page saved
			fpp.close()


			#fll = open('urltable_error.txt', 'w')
			#for i in urltable:
				#fll.write(repr(i) + ' ' + repr(urltable[i]) + '\n')
			#fll.close()
			continue

################ Categori part ##################
# if @ -> save, ignore
# if (number) -> save, add to visit list
#################################################

		hotentryTrue = pty.find('begin of hotEntries')

		if hotentryTrue == -1:
			index_cate = pty.find('begin of categories')
		else: 
			index_cate = hotentryTrue

		# modified 2007.6.25
		#index_cate = pty.find('begin of categories')

		index_cate_end = pty.find('end of categories')
		if index_cate_end == -1:
			index_cate_end = pty.find('end of hotEntries')

		cate = pty [ index_cate : index_cate_end ]

		cate = cate.splitlines()

		lnum = 0		
#		line_number = 0
		for line in cate:
			lnum += 1
			if line.find('href') != -1:
				# href url
				# name of category
				# @ or (number)
				if cate[lnum + 3].find('@') == -1:
					lineurl = line.strip().split('"')[1] 
					fc.write(basehref.split(yahoo_url)[1] + '/' + lineurl + '\n')
					# add to visit list
					tempb = basehref + '/' + lineurl
					Topurl.insert(0, tempb.split(yahoo_url)[1])
				else:
					lineurl = line.strip().split('"')[1] 
					fc.write(lineurl + '\n')

				linename = cate[lnum].strip()  
				fc.write(linename + '\n')
				fc.write(cate[lnum + 3].strip() + '\n')


################################################
################ website part ##################
################################################

		index_web = pty.rfind('mainWebTitle') 
		websites = pty [ index_web : ]
		websites = websites.splitlines()
		flag = False
		lnum = 0
		fp.write('--begin--\n')
		fp.write(repr(CategoryNum) + '\n')

		for line in websites:
			if flag == True and line.find('href') == -1:
				flag = False
				if line.find('</dd>') == -1:
					fp.write(line.strip() + '\n')
				#else:
					#fp.write('\n')
					#fp.write(tmpsite + '\n')

				continue
			if line.find('end of leaves') != -1:
				break
			elif line.find('href') != -1 and line.find('_blank') != -1: 
				flag = True

			# babuk_Player
			#elif line.find('href') != -1 and line.find('http') == -1:
				#flag = True
				#tmpsite = line.split('"')[1]
				#tmpsite = basehref + '/' + tmpsite
				#fp.write('2_article\n')
				#fp.write(line.strip() + '\n')

			elif line.find('<dd>') != -1:
				flag = True
		fp.write('--end--\n')

	# 2007.5.15: if name is comming, it had better remove

	#for i in soup.dd:
		#print i
	#print len(soup.dd)

	#for i in soup.findAll('dd'):
		#print i


	#first, second = soup.findAll('dd')
	#print first, second
	#print soup.prettify()
	fp.close()
	fc.close()

	fl = open('urltable.txt', 'w')
	for i in urltable:
		fl.write(repr(i) + ' ' + repr(urltable[i]) + '\n')
	fl.close()


		#for line in websites:
			#if flag == True and line.find('href') == -1:
				#flag = False
				#if line.find('</dd>') == -1:
					#fp.write(line.strip() + '\n')
				#else:
					#fp.write('\n')
					#fp.write(tmpsite + '\n')

				#continue
			#if line.find('end of leaves') != -1:
			#	break
			#elif line.find('href') != -1 and line.find('_blank') != -1: 
				#flag = True

import sys
import codecs

if __name__ == "__main__":

		
	#for i in dir(soup):
	#	print i

	#print "HEAD:", soup.head

	#try:
		#out = codecs.open(outfile, encoding='euc-kr', mode='w+')
	#except:
		#print "write fail:", outfile
		#raise
		#sys.exit(0)

	myLink()


