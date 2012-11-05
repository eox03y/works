if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		sys.exit()

	f = open(sys.argv[1])
	cnt = 0
	for line in f:
		cnt += 1
	print "%d lines" % (cnt)

