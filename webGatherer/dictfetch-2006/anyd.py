#!/usr/bin/env python

import sys
import os
import cgi
import socket


def test_dict():
	import util
	while 1:
		a = util.getinput("Enter a word:")
		if a=='.': break

		req_dic(a)
		
def req_dic(word):
	msg = "%-4d%s" % (len(word), word)
	sock.send (msg)

	while 1:
		buf = sock.recv (1024)
		if buf == '': break
		print buf
 

def handle_fail():
	print "Sorry, the server is NOT ready. <br/>\n Please try later. <br/>"  


def test_cgi():
	print "<strong>Python %s</strong>" % sys.version
	keys = os.environ.keys( )
	keys.sort( )

	print "<pre>"
	for k in keys:
		print "%s\t%s" % (cgi.escape(k), cgi.escape(os.environ[k]))
	print "</pre>"

if __name__=='__main__':
	import sys
	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	else:
		port = 8080

	
	print 'Content-Type: text/html\n'

	print "<html><head><title>test</title></head><body>"

	#test_cgi()

	forms = cgi.FieldStorage()

	print forms.keys()
	#print forms.values()

	try :
		word = forms['W'].value
	except:
		word = ''
		print "Enter a word"
		print "</body></html>"
 
	#print "port=",port
	print "Word: %s" % word

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sock.connect ( (socket.gethostbyname('localhost'), port) )

		req_dic(word)

	except:
		handle_fail()
		raise

	print "</body></html>"


