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
				idxList[headword] = (offset, body)
			body = ''
			headword = line[2:-1]
		else:
			body += line
		offset += len(line)
	idxList[headword] = (offset, body)
	infd.close()
	return idxList

'''
'''
def	save_sorted_dict(sortedfd, idxlist)
	# sort by the order of headword
	headword_sorted = sorted(idxList.iteritems(), key=lambda x:x[0],  reverse=False)
	offset = 0
	for r in headword_sorted:
		headline = '@ %s\n' % (r[0])
		sortedfd.write(headline)
		sortedfd.write(r[1][1])

		r[1][0] = offset
		offset += len(headline)
		offset += len(r[1][1])
		r[1][1] = len(r[1][1])
	sortedfd.close()
	return headword_sorted
'''
'''
def save_index(outfd, idxList):
	for r in idxList:
		outfd.write('%X\t%X\t%s\n' % (r[1][0], r[1][1], r[0]))
	return result

if __name__=="__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')

	dictfile = sys.argv[1]
	sortedfile = sys.argv[2]
	idxfile = sys.argv[3]
	infd = anyReader.anyReader(dictfile, encoding='ascii')
	sortedfd = anyReader.anyWriter(sortedfile, encoding='ascii')
	idxfd = anyReader.anyWriter(idxfile, encoding='ascii')

	idxlist = make_index_of_dict(infd)
	sortedidx = save_sorted_dict(sortedfd, idxlist)
	save_index(idxfd, sortedidx)
