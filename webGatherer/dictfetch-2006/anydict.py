#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# 영한사전에서 한영 사전을 만든다.
# python의 dict 이용하여 구현.
# dict의 key 는 한글 단어, value = (한글 색인어, 사전 표제어, 의미)
#
# 한글 사전:
# 색인어 = 한글, 데이타 = 영어 단어 목록
# 영어 사전.
# ABCC Atomic Bomb Casualties Commission : x, 원폭 상해 조사 위원회
# --> 색인어 ABCC, 표제어 ABCC Atomic Bomb Casualties Commission

import os.path
import time

import util

from hangul import *
from wndict import *

## a, n, A(자)형의, A형 틀(무거운 물건, 호이스트, 샤프트, 파이프 등을 받치는 데 씀)
## --> remove_in_marks(str, '(', ')' )
## a, n, A형의, A형 틀
def remove_in_marks(str, mark1, mark2):
	res = ''
	pos = 0
	while 1:
		p = str[pos:].find(mark1)
		if p == -1: 
			res += str[pos:]
			break

		else:
			res += str[pos:pos+p]
			pos = pos+p+1

			p = str[pos:].find(mark2)
			if p == -1: break
			pos = pos+p+1

	return res


class anydict:
	
	def __init__(self, wnfile, ehpath, wlistfile):
		self.wnfile = wnfile
		self.ehpath = ehpath
		self.wlistfile = wlistfile
		self.HDICT = {}
		self.EDICT = {}
		self.eWordList = []
	
	def prepare(self, start='a', end='a' ):
		print 'loading EngHan Dict ...'
		t = time.time()
		self.loadEngHanDict(start, end)
		print "Total time %.3f" % (time.time()-t)
		print 'Done'

		print 'loading WordNet Dict ...'
		t = time.time()
		self.loadWordNetDict(self.wnfile)
		print "WordNet %.3f" % (time.time()-t)
		print 'Done'

		print 'loading WordList Dict ...'
		t = time.time()
		self.loadEngWordList(self.wlistfile)
		print "WordList %.3f" % (time.time()-t)
		print 'Done'

		print 'Soring ...'
		self.eWordList.sort()
		print 'Done'

	def __del__(self):
            pass
        
	def prn_hdict(self):
		for (k,v) in self.HDICT.iteritems():
			print "@", k
			for e in v:
				print "  ", e

	def prn_edict(self):
		for (k,v) in self.EDICT.iteritems():
			print "@", k
			for e in v:
        			print "%s : %s" % (e[0], e[1])


	def search_h(self, h):
		try:
			res = ' '.join( self.HDICT[h])
		except:
			res = "not found"

		return res + '\n'

	def search_e(self, e, outfd=None):
		try:
			res = self.prnAnydictItem(self.EDICT[e])
		except:
			res = "not found\n"
		return res

	def search(self, a):
			if ord(a[0]) > 128:
					return self.search_h(a)
			else:
					return self.search_e(a)

	def search_h_prn(self, h):
		try:
			print self.HDICT[h]
		except:
			print "not found"

	def search_e_prn(self, e):
		try:
			self.prnAnydictItem(self.EDICT[e])
		except:
			print "not found"

	def search_prn(self, a):
			if ord(a[0]) > 128:
					#print "한글"
					self.search_h_prn(a)
			else:
					#print "English"
					self.search_e_prn(a)


 
	def info(self):
		print "=== HDICT: %d keys, %d vals" % ( len(self.HDICT), 
			len(self.HDICT) )

		print "=== EDICT: %d keys, %d vals" % ( len(self.EDICT), 
			len(self.EDICT) )

		return

		print self.HDICT.keys()[:4]
		print self.HDICT.values()[:4]
		print self.EDICT.keys()[:4]
		print self.EDICT.values()[:4]
	
	### WordNet 영영 사전 로드
	def loadWordNetDict(self, fname):
		cnt = 0
		init(fname)

		while 1:
			w,expl = next()
			if w == '': break
			cnt += 1

			#print w, expl
			html = proc_oneword(w, expl)
			self.insertE_EE(w, html)
			#if cnt > 4: break
		
		print "Total:", cnt

	## 영어 단어 목록 파일에서 단어의 원형, 명사형 등 연관 단어 찾기
	def loadEngWordList(self, fname):
		try:
			fd = open(fname, 'r')
		except:
			print "reading failed:", fname

		for line in fd.xreadlines():
			sp = line.split(':')
			if len(sp) < 2: continue

			sp2 = sp[1].split()
			if len(sp2) > 7:
				self.insertE_related(sp[0].strip(), sp2[7])



	## 영한 사전: 알파벳별로 화일 분리되어 있음. -- 루프.
	## 다른 사전보다 제일 먼저 로드해야 한다.
	def loadEngHanDict(self, start, end):	
		for alpha in range(ord(start), ord(end)+1):
			fname = os.path.join(self.ehpath, chr(alpha) + ".dic")
			
			t = time.time()
			self.oneEngHanDict(fname)
			print "EngHan %.3f" % (time.time()-t)


	## 영한 사전 화일 하나 처리
	def oneEngHanDict(self, fname):
		try:
			fd = open(fname, 'r')
		except:
			print "reading failed:", fname
	
		n = 0
		for line in fd.xreadlines():
			self.parseEngHanDict(line)
			n += 1
			#if n > 5: return
		print "%d word from %s" % (n, fname)

	## 복합단어 처리
	def stemHanComplex(self, word):
		basewords = stem_complex(word)

		res = []
		for b in basewords:
			if self.HDICT.has_key(b):		
				res.append(b)

		return res
			

	def getEngIndexWord(self, head):
		s = head.split()
		if len(s) > 2 and s[0].isupper(): 
		# 대문자 약어이면 약어만 색인어로 한다.
			return s[0]

		p = head.find(',')
		if p != -1:
			return head[:p-1]	
		else:
			return head

	def parseEngHanDict(self, line):
		s = line.split(":")

		if len(s) < 2: 
			print "error :"
			print line
			return

		head = s[0].strip()
		expl = s[1].strip()

		idxword = self.getEngIndexWord(head)

		item = (head, expl)
		#print idxword
		self.insertE_EH(idxword, item)

		hwords = self.get_han_stem(expl)
		for h in hwords:
			self.insert_h_item(h, idxword)

	
	def get_han_stem(self, expl):
	# return 한글 색인어 목록. 라인에서 한글만 구한 다음 처리.
		stems = []

		expl = remove_in_marks(expl, '(', ')')
		hwords = filterHanWords(expl)

		## 영어 단어 설명에 나오는 모든 하글 단어에 대해
		## stem을 구한다.
		for h in hwords:
			for stem in stemHanWord(h):
				stems.append(stem)

				if len(stem) > 6: ## 복합단어
					#stems += self.stemHanComplex(stem)	
					pass
					
		return stems


	## 영어 단어 목록 파일에서 단어의 원형, 명사형 등 연관 단어 찾기
	def	insertE_related(self, word, related):
		try:
			self.EDICT[word][0] = related
		except:
			pass

	## 영한 사전에서 구한 영어 단어 넣기
	def insertE_EH(self, key, item):
		try:
			self.EDICT[key][2].append(item)
			print "Multi EH:", key
		except:
			newone = [None]* 6
			newone[2] = [item]
			self.EDICT[key] = newone
			self.eWordList.append(key)
		pass

	## 영한 사전에서 구한 영어 단어 넣기
	def insertE_EE(self, key, expl):
		try:
			self.EDICT[key][1] = expl
		except:
			newone = [None]* 6
			newone[1] = expl
			self.EDICT[key] = newone
			self.eWordList.append(key)
		pass

	def insert_h_item(self, key, item):
		try:
			ewords = self.HDICT[key]
			if item not in ewords:
				ewords.append(item)
		except:
			self.HDICT[key] = [item]
		pass

	
	###
	def prnAnydictItem(self, item):
		if item[0] == None: item[0] = ''

		res = "%s\n%s\n%s : %s\n" % ( item[0], item[1], item[2][0][0], item[2][0][1])

		print '-'*10, "관련"
		if item[0] != None: print item[0]
		print '-'*10, "영영"
		print item[1]
		print '-'*10, "영한"
		for eh in item[2]:
			print "%s : %s" % (eh[0], eh[1])

		return res
	
	def testit(self):
		while 1:
			a = util.getinput("Enter a word:")
			if a=='.': break
			if a=='': continue

			self.search_prn(a)
	


if __name__ == "__main__":
	if os.getenv("SHELL") != None:
		hdic = anydict (
			"/data1/AD/data/wn17.dict",
			"/data1/AD/data/engdic/",
			"/data1/AD/data/word.dict"
		)
	else:
		hdic = anydict("C:/Works/ad_svc_backup/ad_svc_data/engdic/")

	hdic.prepare('a', 'z')

	hdic.info()
	#hdic.prn_hdict()
	#hdic.prn_edict()

	hdic.testit()



