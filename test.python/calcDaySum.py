# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:20:18 2013

@author: daehee00.han
"""
import csv
import cStringIO
import codecs
import sys
import time
import datetime
import operator
import handolUtil
import pymongo

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(str(s), 'utf-8').encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def store_csv():
    coll = { "_id" : "20130101", "한ac" : [ 472732, 180190, 300, 776523, 424882 ], "Nil" : [ 386067, 22, 51741, 216, 50 ], "pop" : [ 114318, 16415, 312, 92744, 31685 ], "tag" : [ 15758, 5492, 44, 41135, 12842 ], "iqry" : [ 1958729, 377261, 168494, 1983558, 822801 ], "null" : [ 45106, 2, 4086, 4, 2 ] }
    r = coll
    heads = [[k]*len(v) for k,v in r.iteritems() if k!="_id"]
    vals = [v for k,v in r.iteritems() if k!="_id"]
    headsall = reduce(lambda x,y: x+y, heads)
    onerecord = reduce(lambda x,y: x+y, vals)
    headsall.insert(0, 'date')
    onerecord.insert(0, r['_id'])
    print headsall
    print onerecord
    
    fname = "t.csv"
    outf = open(fname, 'wb')
    writer = csv.writer(outf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer = UnicodeWriter(outf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headsall)
    writer.writerow(onerecord)




def connectMongo():
	c = pymongo.Connection('localhost', 27018)
	db = c['qclog2013']
	return db


def concat_list(x,y):
	if type(x)!=list: x = [x]
	if type(y)!=list: y = [y]
	return x + y

def get_list_len(x):
	if type(x)!=list: return 1
	return len(x)
	

"""
> use qclog2013
switched to db qclog2013
> db.im.find({"_id":"20130101"})
{ "_id" : "20130101", "ac" : [ 472732, 180190, 300, 776523, 424882 ], "Nil" : [ 386067, 22, 51741, 216, 50 ], "pop" : [ 114318, 16415, 312, 92744, 31685 ], "tag" : [ 15758, 5492, 44, 41135, 12842 ], "iqry" : [ 1958729, 377261, 168494, 1983558, 822801 ], "null" : [ 45106, 2, 4086, 4, 2 ] }
"""
def save_collection_to_csv(coll, fname):
    
    # read from mongoDB
    reslist = []
    n = 0    
    for r in coll.find():        
        if n==0:
            heads = [[k]*get_list_len(v) for k,v in r.iteritems() if k!="_id"]
            headsall = reduce(concat_list, heads)
            headsall.insert(0, 'date')
            reslist.append(headsall)            
            
        vals = [v for k,v in r.iteritems() if k!="_id"]        
        onerecord = reduce(concat_list, vals)        
        onerecord.insert(0, r['_id'])
        reslist.append(onerecord)
        n += 1
    
        #print headsall
        #print onerecord

    # save to CSV file
    outf = open(fname, 'wb')
    #writer = csv.writer(outf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer = UnicodeWriter(outf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #writer.writerow(headsall)
    #writer.writerow(onerecord)
    for r in reslist:
        writer.writerow(r)
    outf.close()

#
def main():
    db = connectMongo()
    for collname in ['info', 'im', 'devtype', 'dm', 'dos', 'osshop', 'shop']:
        coll = db[collname]
        fname = "report.%s.csv" % (collname)
        save_collection_to_csv(coll, fname)
	print "--> %s" % (fname)

if __name__ == '__main__':
    main()
