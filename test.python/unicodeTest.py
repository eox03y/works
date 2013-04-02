#!/usr/bin/env python
## -*- coding: EUC-KR -*-

# 2006. 11.23


import sys
import codecs

def printField1(filename, length):
	fp = codecs.open(filename, 'rb', encoding='utf-8')
	errcnt = 0
	numList = []
	for i,line in enumerate(fp):
		sline = line.split('|@')
		#if len(sline) != length or not sline[4].isdigit():
		#	errcnt += 1
			#print '[%d](%d Fields)' % (i+1, len(sline))
			#print line
		numList.append(len(sline))
	fp.close()
	print "%s ==> %d odd lines" % (filename, errcnt)
	return numList

def printField2(filename, length):
	fp = open(filename, 'rb')
	errcnt = 0
	numList = []
	for i,line in enumerate(fp):
		uline = unicode(line, 'utf-8')
		flds1 = line.split('|@')
		flds2 = uline.split('|@')
		if len(flds1) != len(flds2):
			print "[%d] %s" %(i,line)
			errcnt += 1
		numList.append(len(flds1))
		
	fp.close()
	print "%s ==> %d odd lines" % (filename, errcnt)
	return numList

if __name__ == '__main__':

	if len(sys.argv) == 3:
		A = printField1(sys.argv[1], int(sys.argv[2]))
		B = printField2(sys.argv[1], int(sys.argv[2]))
		for i,a in enumerate(A):
			if a != B[i]:
				print "ERR[%d] %d,%d" % (i, a,B[i])
			

	else:	
		print 'Usuage: python verifyFields.py Input_file Field_length'
		sys.exit(0)



