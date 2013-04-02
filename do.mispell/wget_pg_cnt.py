import os
for i in range(24):
	url = "http://dumps.wikimedia.org/other/pagecounts-raw/2013/2013-03/pagecounts-20130301-%02d0000.gz" % (i)
	print url
	os.popen("wget %s" % (url))
