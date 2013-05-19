# -*- coding: utf-8 -*-
import codecs
import sys
import re
import anyReader


'''
'''
def	read_dict(dictfd, offset, length):
	dictfd.seek(offset)
	content = dictfd.read(length)
	return content

'''
'''
def load_index(idxfd):
	idxlist = {}
	for line in idxfd:
		flds = line.split('\t')
		headword = flds[2].rstrip()
		offset = int(flds[0], 16)
		length = int(flds[1], 16)
		idxlist[headword] = (offset, length)
	idxfd.close()
	return idxlist

def test_idx(dictfd, idxlist):
	while True:
		word = raw_input('Enter a word:')
		info = idxlist.get(word, None)
		if not info: print 'NO word'
		else: print read_dict(dictfd, info[0], info[1])


if __name__=="__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')

	dictfile = sys.argv[1]
	idxfile = sys.argv[2]
	dictfd = anyReader.anyReader(dictfile, encoding='ascii')
	idxfd = anyReader.anyReader(idxfile, encoding='ascii')

	idxList = load_index(idxfd)
	test_idx(dictfd, idxList)

