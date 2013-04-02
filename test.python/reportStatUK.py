import sys
import time
import datetime
from operator import itemgetter
import handolUtil
import pymongo
import codecs


def connectMongo():
	c = pymongo.Connection('localhost', 27018)
	db = c['qclog2013']
	db = c['test']
	return db


"""
db.keywords.find({"20130131.234.r":0})
MCC 234 -- UK
MCC 450 -- Korea
"""
def doit_per_MCC(MCC, outf):
	db = connectMongo()
	res=[]
	for data in db.keywords.find():
		if not data["20130131"].get(MCC, None):
			continue
		uk = data["20130131"][MCC]
		my = [data["_id"], uk["q"], uk["c"], uk["r"]]
		res.append(my)

	print "MCC %s: %d" % (MCC, len(res))

	res = sorted(res,  key=lambda x:x[1], reverse=True)

	outf =  codecs.open(outf, "wb", encoding='utf-8')
	for v in res:
		line = "%d , %d , %d , " % (v[1], v[2], v[3])	
		outf.write(line)
		outf.write(v[0])
		outf.write("\n")
	outf.close()

if __name__=="__main__":
	doit_per_MCC(sys.argv[1], sys.argv[2])

		 

