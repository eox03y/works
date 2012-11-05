#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# 웹에서 각종 용어 사전 데이타를 모으기 위한 기본 클래스 정의


def isalphaonly(str):
	for ch in str:
		if not ch.isalpha(): return 0
	return 1

NOPHRASE = 0x01
NOCASE = 0x02

class fetchdic:
	
	def __init__(self, dataFile):
		self.finishword = finishword

		try:
			self.dataFd = open(dataFile, 'w')
		except:
			print "failed in writing file : ", indexFile
			return


	
	def __del__(self):
		self.fd.close()

	def main(self):


	def enqueueDoc(self):
		pass

	def processDoc(self):
		pass

	def storeData(self, idxword, sndword, expl):
	# idxword - 표제어, 색인어
	# sndword - second word. 색인어 의 유사어
	# expl - 설명문, 번역문 등
		pass


if __name__ == "__main__":


