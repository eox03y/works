import urlparse
url = 'HTTP://www.Python.org/doc/#'
print urlparse.urlsplit(url)

url = 'HTTP://www.Python.org/doc/ad.dic?hello=hihi#abc'
r =  urlparse.urlsplit(url)
print r

cleanurl = "%s::/%s%s" % r[:3]
print cleanurl


url = 'HTTP://www.Python.org/doc/ad.dic?hello=hihi#abc'
r =  urlparse.urlparse(url)
print r
