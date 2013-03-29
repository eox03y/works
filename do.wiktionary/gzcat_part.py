import sys
import codecs


"""
usage: %prog num_of_lines input_file output_file
"""

n_lines = int(sys.argv[1])
# read/write gzip file
reader=codecs.getreader("utf-8")
writer=codecs.getwriter("utf-8")

# two input files given, one output file given
if sys.argv[2].endswith(".gz"):
	import gzip
	A=reader(gzip.open(sys.argv[2], 'rb'))
elif sys.argv[2].endswith(".bz2"):
	import bz2
	bz2fd = bz2.BZ2File(sys.argv[2], 'rb')
	A=reader(bz2fd)
else:
	A=reader(open(sys.argv[2], 'rb'))

C=writer(open(sys.argv[3], 'wb'))

cnt = 0
for line in A:
	C.write(line)
	cnt += 1	
	if cnt >= n_lines: break

A.close()
C.close()
