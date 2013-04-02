import time
import datetime

def timedelta2float(td):
	res = td.microseconds/float(1000000) + (td.seconds + td.days * 24 * 3600)
	return res

def timedelta2int(td):
	res = round(td.microseconds/float(1000000)) + (td.seconds + td.days * 24 * 3600)
	return res

dateval1 = datetime.datetime.strptime("25-01-2013 00:00:03:238", "%d-%m-%Y %H:%M:%S:%f")
dateval2 = datetime.datetime.strptime("25-01-2013 00:00:03:950", "%d-%m-%Y %H:%M:%S:%f")
dateval3 = datetime.datetime.strptime("25-01-2013 00:01:04:614", "%d-%m-%Y %H:%M:%S:%f")
diff1 = dateval2 - dateval1
diff2 = dateval3 - dateval1
print "datetime:", diff1
print timedelta2float(diff1)
print timedelta2int(diff1)
print

print "datetime:", diff2
print timedelta2float(diff2)
print timedelta2int(diff2)
print


oneday = datetime.timedelta(days=1)
print timedelta2float(oneday)
print timedelta2int(oneday)
print
