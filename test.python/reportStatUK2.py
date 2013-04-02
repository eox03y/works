import sys
import time
import datetime
import operator
import handolUtil
import pymongo
import codecs


def connectMongo():
	c = pymongo.Connection('localhost', 27018)
	db = c['test']
	return db


"""
db.keywords.find({"20130131.234.r":0})
MCC 234 -- UK
MCC 450 -- Korea
"""


def get_sum_days(days, perday, MCC):
	res = [0,0,0]
	for day in days:
		try:
			val = perday[day][MCC]
		except:
			continue
		vals = [val["q"], val["c"], val["nores"]]	
		res = map(operator.add, res, vals)	
	return res
			
		
def doit_per_MCC(days):
	db = connectMongo()
	#day = '20130125'
	kor_list = []
	uk_list = []
	for data in db.keywords.find():
		kor_sum = get_sum_days(days, data, "450")					
		uk_sum = get_sum_days(days, data, "234")					
		if kor_sum[0] > 0:
			kor_list.append([data["_id"]] + kor_sum)
		if uk_sum[0] > 0:
			uk_list.append([data["_id"]] + uk_sum)
			
	write_report(kor_list, "KOR.keywords.csv")
	write_report(uk_list, "UK.keywords.csv")

def write_report(rep_list, outf):
	res = sorted(rep_list,  key=lambda x:x[1], reverse=True)
	outf =  codecs.open(outf, "wb", encoding='utf-8')
	n = 0
	for v in res:
		line = "%d , %d , %d , " % (v[1], v[2], v[3])	
		outf.write(line)
		outf.write(v[0])
		outf.write("\n")
		n += 1
		#if n > 150: break
	outf.close()

if __name__=="__main__":
	daylist = handolUtil.get_day_list('2013-01-01', '2013-02-01')

	doit_per_MCC(daylist)

		 

