
import os
import sys

#python beautiful.py  link http://www.auction.co.kr/category/category01.html aution01.txt
def do_auction(num):
	cmd = "python beautiful.py  link http://www.auction.co.kr/category/category%02d.html auction%02d.txt" % (num, num)
	os.system(cmd)

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "usage start_num end_num"
		sys.exit(0)
	for i in range(int(sys.argv[1]), int(sys.argv[2])+1):
		print i
		do_auction(i)

