# -*- coding: utf-8 -*-
import codecs
import sys
import re
import anyReader

'''
infd : input file descriptor
'''
def make_index_of_dict(infd):
	idxList = {} # output; the index of words in dict file

	offset = 0
	headword = None
	body = ''
	for line in infd:
		if line[0]=='@':
			if headword:
				idxList[headword] = (offset, len(body))
			body = ''
			headword = line[2:-1]
		else:
			body += line
		offset += len(line)
	idxList[headword] = (offset, len(body))
	return idxList

def save_index(outfd, idxList):
	result = sorted(idxList.iteritems(), key=lambda x:x[0],  reverse=False)
	for r in result:
		outfd.write('%X\t%X\t%s\n' % (r[1][0], r[1][1], r[0]))


if __name__=="__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')

	dictfile = sys.argv[1]
	outfile = sys.argv[2]
	infd = anyReader.anyReader(dictfile, encoding='ascii')
	outfd = anyReader.anyWriter(outfile, encoding='ascii')
	idxlist = make_index_of_dict(infd)
	save_index(outfd, idxlist)
