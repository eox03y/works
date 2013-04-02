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
	return db


"""
db.keywords.find({"20130131.234.r":0})
MCC 234 -- UK
MCC 450 -- Korea
"""
def doit_per_MCC(day, outf):
	db = connectMongo()
	#day = '20130125'
	res=[]
	listPerMcc = {}
	for data in db.keywords.find():
		permcc = data.get(day, None)
		if not permcc: continue
		for mcc,val in permcc.iteritems():
			if type(val)!=dict: continue
			wlist = listPerMcc.get(mcc, [])
			if wlist==[]: listPerMcc[mcc] = wlist
			wlist.append([data["_id"], val["q"], val["c"], val["nores"]])
			

	outf =  codecs.open(outf, "wb", encoding='utf-8')
	for mcc,wlist in listPerMcc.iteritems():
		outf.write("MCC , %s" % (mcc))	
		outf.write("\n")
		res = sorted(wlist,  key=lambda x:x[1], reverse=True)
		n = 0
		for v in res:
			line = "%d , %d , %d , " % (v[1], v[2], v[3])	
			outf.write(line)
			outf.write(v[0])
			outf.write("\n")
			n += 1
			if n > 150: break
	outf.close()

if __name__=="__main__":
	doit_per_MCC(sys.argv[1], sys.argv[2])

		 

