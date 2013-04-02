import codecs
import sys
reader = codecs.getreader("utf-8")
input = reader(sys.stdin)
writer = codecs.getwriter("utf-8")
output = writer(sys.stdout)
for line in input:
	if not line[3].isalpha(): continue

	flds = line.split()
	if len(flds) != 4: continue 
	if len(flds[1]) > 30: continue 
	#if not flds[1][0].isalpha(): continue
	visit_cnt = int(flds[2])
	bytes = int(flds[3])
	if bytes < 1024*20: continue	
	if visit_cnt < 10: continue	
	if flds[1].find('(') != -1: continue
	output.write(u"%s\t%s\n" % (flds[1], flds[2]))
