# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      daehee00.han
#
# Created:     19-02-2013
# Copyright:   (c) daehee00.han 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import codecs
import operator
import handolUtil
from operator import itemgetter

"""
Compute the Damerau-Levenshtein distance between a given string s1
and many other strings s2.
"""
class DLDistance:
	def __init__(self, s1):
		self.s1 = s1
		self.d = {}
		self.lenstr1 = len(self.s1)
		for i in xrange(-1,self.lenstr1+1):
			self.d[(i,-1)] = i+1

	def distance(self, s2):
		lenstr2 = len(s2)
		for j in xrange(-1,lenstr2+1):
			self.d[(-1,j)] = j+1

		for i in xrange(self.lenstr1):
			for j in xrange(lenstr2):
				if self.s1[i] == s2[j]:
					cost = 0
				else:
					cost = 1
				self.d[(i,j)] = min(
							   self.d[(i-1,j)] + 1, # deletion
							   self.d[(i,j-1)] + 1, # insertion
							   self.d[(i-1,j-1)] + cost, # substitution
							  )
				if i and j and self.s1[i]==s2[j-1] and self.s1[i-1] == s2[j]:
					self.d[(i,j)] = min (self.d[(i,j)], self.d[i-2,j-2] + cost) # transposition

		return self.d[self.lenstr1-1,lenstr2-1]

###
class DictDict:
	def __init__(self):
		self.D = {}

	def insert(self, keyword, val):
		if len(keyword) < 4: return
		firstkey = keyword[:2]
		secondD = self.D.get(firstkey, {})
		if secondD=={}:
			self.D[firstkey] = secondD
		secondD[keyword] = val

	def search(self, keyword):
		if len(keyword) < 4: return None
		firstkey = keyword[:2]
		try:
			val = self.D[firstkey][keyword]
		except:
			return None

	def searchNearest(self, keyword, k_freq):
		""" search the nearest (DL-distance) word for a given word (keyword)
		"""
		if len(keyword) < 4: return None
		firstkey = keyword[:2]
		keylist = self.D.get(firstkey, None)
		if keylist==None: return None

		#res = []
		highq = 0
		foundk = None
		foundd = 10
		dl = DLDistance(keyword)
		for k,v in keylist.iteritems():
			# frequency of high-ranked keyword must be more than 10 times
			if v[0] < k_freq * 10: continue		
			dist = dl.distance(k)
			if dist <= 2:
				if v[0] > highq:
					highq = v[0]
					foundk = k
					foundd = dist
					foundnores = v[1]
				#res.append((dist, k, v[0], v[1]))

		#if len(res)==0: return None
		#return res

		if foundk==None: return None
		return [(foundd, foundk, highq, foundnores)]
###
def load_keywords_stat(fname, resfname, wikif):
	"""
	"""
	watch = handolUtil.StopWatch()
	print "Loading ...", wikif
	wikiStat = {}
	fp = codecs.open(wikif, 'rb', encoding='utf-8')
	for line in fp:
		flds = line.split()
		w = flds[0].lower().replace('_', ' ')
		n = int(flds[1])
		if not wikiStat.has_key(w):
			wikiStat[w] = n	

	fp.close()
	print "Loaded: %f" % (watch.laptime())
	
	"""
	== keywords.stat
	3997563 270333  6410    facebook
	2399787 186241  45449   whatsapp
	1433213 71764   1458    whats app
	1315718 130860  2040    temple run
	1004372 163723  272     games
	947351  87185   19846   skype
	829801  316731  834     angry birds
	529552  64385   1416    fruit ninja
	"""
	print "Loading ...", fname
	highKeywords = DictDict()
	noresKeywords = []
	fp = codecs.open(fname, 'rb', encoding='utf-8')
	for line in fp:
		flds = line.split('\t')
		q = int(flds[0])
		c = int(flds[1])
		nores = int(flds[2])
		keyword = flds[3].strip()
		kflds = keyword.split()
		if len(kflds) > 2: continue
		noresratio = (nores*100)/q

		if q > 10 and noresratio > 50:
			if not wikiStat.has_key(keyword):
				noresKeywords.append([keyword, q, noresratio])
		if q > 150 and noresratio < 4:
			highKeywords.insert(keyword, [q, noresratio])
	fp.close()
	print "Loaded: %f" % (watch.laptime())
	print "noresKeywords: %d" % (len(noresKeywords))
	print "highKeywords: %d" % (len(highKeywords.D))

	fp = codecs.open(resfname, 'wb', encoding='utf-8')
	for noresK in noresKeywords:
		nearest = highKeywords.searchNearest(noresK[0], noresK[1])
		if nearest:
			prnformat = u'\t'.join(map(lambda (d,x,y,z):"%d\t%s\t%d\t%d" % (d, x,y,z), nearest))
			fp.write("%s\t%d\t%d\t%s\n" % (noresK[0], noresK[1], noresK[2], prnformat))
	fp.close()
	print "Processed: %f" % (watch.laptime())


def main():
    load_keywords_stat('./keywords.stat', './keyword.correction', './all.org.en')
    pass

if __name__ == '__main__':
    main()
