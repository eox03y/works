#!/usr/bin/env python
# -*- coding: euc-kr -*-
import urlparse
import geturl
import BeautifulSoup


def get_text(htmltree):
	text = ""
	for item in htmltree:

		#print item, item.__class__.__name__
		if item.__class__.__name__ == "Tag":
			text += get_text(item)
		else:
			text += item
	return text


def saveLink(soup, tagname, out):
	for link in soup(tagname):
		#print link
		try:
			out.write(link['href'])
			out.write('\t')
		except:
			continue

		#print link.contents
		try:
			link_name = get_text(link.contents)
			link_name = link_name.strip()
			#print link_name
			out.write(link_name)
			out.write('\n')
		except:
			pass


# 연속된 빈 라인 제거를 위해 .
class trimLines:
	def __init__(self):
		self.cnt = 0
		self.prevEmpty = False

	def filter(self, line):
		isThisGoodLine = True
		t = line.strip()
		if len(t) == 0:
			if self.prevEmpty:
				isThisGoodLine = False		
			self.prevEmpty = True
		else:
			self.prevEmpty = False
		return isThisGoodLine
		

# BeautifulSoup 를 이용하여 텍스트만 추출하기
def getOnlyText(soup, outEnc='euc-kr'):
	#getting all comments 
	comments = soup.findAll(text=lambda text:isinstance(text, BeautifulSoup.Comment)) 

	# deleting all comments 
	[comment.extract() for comment in comments] 

	# delete script
	c=soup.findAll('script') 
	for i in c:
		i.extract()


	# get only the text from the <body> 
	body = soup.body(text=True) 

	trim = trimLines()
	body = [b.encode(outEnc, 'ignore') for b in body if trim.filter(b)]
	text = ''.join(body) 
	return text
	


def url2txt(url, outEnc='euc-kr'):
	srcType, srcEnc, srcHtml = geturl.geturl(url)
	
	print srcEnc
	soup = BeautifulSoup.BeautifulSoup(srcHtml, fromEncoding=srcEnc[0], convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
	txt = getOnlyText(soup, outEnc)
	return txt


class url2text:
	def __init__(self, url, outEnc='euc-kr'):
		self.srcUrl= url
		self.srcType = ''
		self.srcHtml = ''
		self.outEnc = outEnc 
		self.text = ''

	def getText(self):
		self.srcType, self.srcEnc, self.srcHtml = geturl.geturl(self.srcUrl)
		
		#self.srcHtml = self.srcHtml.replace("<br>","\n")
		#self.srcHtml = self.srcHtml.replace("<br/>","\n")

		print self.srcEnc[0]
		self.soup = BeautifulSoup.BeautifulSoup(self.srcHtml, 
											fromEncoding=self.srcEnc[0], 
											convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
		self.text = getOnlyText(self.soup, self.outEnc)
		return self.text
		

	def getMainContent(self):
		if self.text == '':
			self.getText()
		self.getLinks()
		self.getAbsLinks()
		cmpU = url2text(self.getCmpUrl())
		cmpU.getText()
		return cmpTwoTexts(self.text, cmpU.text)
		
	def getLinks(self):
		def filterLink(link):
			try:
				link['href']
				return True
			except:
				return False
	
		self.links = [link['href'] for link in self.soup('a') if filterLink(link) ]
		return self.links

	def getAbsLinks(self):

		self.links = map(lambda link: urlparse.urljoin(self.srcUrl, link), self.links)
		return self.links

	def getCmpUrl(self, debug=False):
		orgurl = urlparse.urlsplit(self.srcUrl)
		if debug: print orgurl
		
		cleanurl = "%s://%s%s" % orgurl[:3]
		if debug: print cleanurl

		for link in self.links:
			if link.startswith(cleanurl) and not link.startswith(self.srcUrl):
				if debug: print "ORG: %s\nCMP: %s" % (self.srcUrl, link)
				return link
		return ''

	def prnLinks(self):
		print "==============="
		for link in self.links:
			print link
		print "==============="


def cmpTwoTexts(textA, textB):
	A = textA.splitlines()
	B = textB.splitlines()
	A = map(str.strip, A)
	B = map(str.strip, B)

	begin = 0
	while begin < len(A):
		if A[begin] != B[begin]: break
		begin += 1

	end = -1
	while end > 1-len(A):
		if A[end] != B[end]: break
		end -= 1

	print "LINES=%d, B=%d, E=%d" % (len(A), begin, end)

	return "\n".join(A[begin:end+1])

	


import sys
import codecs

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: url outfile"
		sys.exit(0)

	outEncoding = 'euc-kr'
	u2t = url2text(sys.argv[1], outEncoding)
	txt = u2t.getMainContent()

	try:
		outfile = sys.argv[2]
		#out = codecs.open(outfile, encoding=outEncoding, mode='w+')
		out = open(outfile, mode='w+')
		out.write(txt)
		out.close()
	except:
		print "write fail:", outfile
		raise
		sys.exit(0)



