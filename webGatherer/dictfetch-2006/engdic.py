#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# 영어 단어 목록 iterator 제공


def isalphaonly(str):
	for ch in str:
		if not ch.isalpha(): return 0
	return 1

NOPHRASE = 0x01
NOCASE = 0x02

class engdic:
	
	def __init__(self, dictfile, mode=0, startword='', finishword=''):
		self.end = 0
		self.lastword = ""
		self.mode = mode
		self.startword = startword
		self.finishword = finishword

		try:
			self.fd = open(dictfile, 'r')
		except:
			print "failed in reading dict file : ", dictfile
			return

		self._skip()
	
	def __del__(self):
		self.fd.close()


		
	def _skip(self):
		if self.startword != '':
			## 시작 단어까지 skip
			for line in self.fd.xreadlines():
				if line.startswith(self.startword): break

	## return '' if no more reading.
	def next(self):
		if self.end: return ''
		word = ''

		for line in self.fd.xreadlines():
			if not line[0].isalpha(): continue

			str = line.split(':')[0]
			word = str.split()
			
			if len(word) > 1:
				if self.mode & NOPHRASE: continue
				word = ' '.join(word)
                        else:
           			word = word[0]
				if not isalphaonly(word): continue

			if self.mode & NOCASE:
				word = word[0].lower()

			if word == self.lastword: continue
			self.lastword = word

			#print word
			break

		## 종료 단어 체크
		if self.finishword != '' and word == self.finishword: 
			self.end = 1

		return word

if __name__ == "__main__":
	edict = engdic("c:/Works/ad_svc_backup/word.dict", 
			#NOCASE | NOPHRASE )
                      NOPHRASE )
	print edict.next()
	print edict.next()


