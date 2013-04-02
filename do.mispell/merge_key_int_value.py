import sys
import codecs
import gzip
"""
Input Assumption: 
	A,B are utf-8 files.
	A,B contain key-value pair, and the value is integer type. 
	A,B are sorted by key.
Output: sorted key-value pair
"""
#A=codecs.open(sys.argv[1], 'rb', encoding='utf-8')
#B=codecs.open(sys.argv[2], 'rb', encoding='utf-8')
#C=codecs.open(sys.argv[3], 'wb', encoding='utf-8')

# read/write gzip file
reader=codecs.getreader("utf-8")
writer=codecs.getwriter("utf-8")
A=reader(gzip.open(sys.argv[1], 'rb'))
B=reader(gzip.open(sys.argv[2], 'rb'))
C=writer(gzip.open(sys.argv[3], 'wb'))

flda = None
fldb = None

while True:
	if not flda:
		try:
			linea = A.next()	
			flda = linea.split()
		except:
			for lineb in B: C.write(lineb)
			break
	
	if not fldb:
		try:
			lineb = B.next()	
			fldb = lineb.split()
		except:
			for linea in A: C.write(linea)
			break

	if flda[0] < fldb[0]:
		C.write(linea)	
		flda = None
	elif flda[0] > fldb[0]:
		C.write(lineb)	
		fldb = None
	else:
		newval = int(flda[1]) + int(fldb[1])
		C.write(u"%s %d\n" % (flda[0], newval))	
		flda = None
		fldb = None

				

	

