import pymongo
import handolUtil
#c = pymongo.MongoClient('localhost', 27018)
c = pymongo.Connection('localhost', 27018)
print c
db = c['qclog2013']
print db

print db.keywords
print db.days
coll = db['keywords']
coll = db['test']
print coll


d = handolUtil.AddValueDict()
d.add('iqry', [1, 0])
d.add('iqry', [1, 1])
d.add('iqry', [1, 0])
d.add('ac', [1, 1])
d.add('ac', [1, 1])
d.add('', [1, 0])

day='20130131'

#coll.insert({"_id":day, "vals": d})


dd = dict(d)
dd["_id"] = day
coll.insert(dd)

print coll.insert(dd)
found = coll.find_one(dd)
print "found", found
found = coll.find_one({"_id":day})
print "found", found

dd['new'] = 100
print coll.update({"_id":day}, {"$set":{"iqry":200, "new":100}})

d = {}
keyword="aaa"
day = "20130214"
newdata = [1,2,4]
day = "20130213"
newdata = [1,2,3]
day = "20130215"
newdata = [1,2,5]
newdic = {day:newdata}

d["_id"] = keyword

found = coll.find_one({"_id":keyword})
print "found", found
if found:
	old = found.get("perday", {})
	old[day] = newdata
	coll.update({"_id":keyword}, {"$set":{"perday":old}})
else:
	
	coll.insert({"_id":keyword, "perday":newdic})
