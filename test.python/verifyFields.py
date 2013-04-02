#!/usr/bin/env python
## -*- coding: EUC-KR -*-

# 2006. 11.23


import sys

def printField(filename, length):
	'result 를 바탕으로 특정 field를 프린트한다'

	try:
		fp = open(filename, 'r')

	except:
		print 'No exist file'
		sys.exit(0)

	errcnt = 0
	for i,line in enumerate(fp):
		sline = line.split('|@')
		if len(sline) != length:
			errcnt += 1
			print '[%d](%d Fields)' % (i+1, len(sline))
			print line
	fp.close()

	print "%s ==> %d odd lines" % (filename, errcnt)


if __name__ == '__main__':

	if len(sys.argv) == 3:
		printField(sys.argv[1], int(sys.argv[2]))

	else:	
		print 'Usuage: python verifyFields.py Input_file Field_length'
		sys.exit(0)



