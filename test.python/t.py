import time
import datetime

dateval1 = time.strptime("25-01-2013 00:00:03:238", "%d-%m-%Y %H:%M:%S:%f")
dateval2 = time.strptime("25-01-2013 00:00:03:938", "%d-%m-%Y %H:%M:%S:%f")
print dateval1
#print "time:", dateval2 - dateval1

dateval1 = datetime.datetime.strptime("25-01-2013 00:00:03:238", "%d-%m-%Y %H:%M:%S:%f")
dateval2 = datetime.datetime.strptime("25-01-2013 00:00:03:938", "%d-%m-%Y %H:%M:%S:%f")
print "datetime:", dateval2 - dateval1


oneday = datetime.timedelta(days=1)
print oneday


a=[
	[1,2,3]
	,[10,20,30]
]


import operator
s=[0]*len(a[0])
for i in a:
	s = map(operator.add, s, i)
	print s


d = {'a':10, 'c':20, 'b':30}
for k,v in d.iteritems():
	print k,v

ranked = sorted(d.iteritems(), key=lambda x:x[1],  reverse=True)
e = ranked[0]
print e
print e[0], e[1]
for k,v in ranked:
	print k,v
