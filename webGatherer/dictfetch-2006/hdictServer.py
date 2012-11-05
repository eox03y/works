#!/usr/bin/env python

import sys
import os
#import time
import SocketServer

from daemon import daemonize
from anydict import anydict


class MyHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		while 1:
			lenpart = self.request.recv(4)
			if not lenpart: break

			print "LEN:", lenpart
			msglen = int(lenpart)

			msg = self.request.recv(msglen)
			print "MSG:", msg

			if not msg: break

			if len(msg) != msglen:
				print "read msg incompletely"

			print msg
			res = search(msg)
			self.request.send(res)
			break





def search(msg):
	return hdic.search(msg)


def main(portnum):
	myServer = SocketServer.TCPServer(('',8080), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )


if __name__=='__main__':
	#time.sleep(1);
	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	else:
		port = 8080

	if os.getenv("SHELL") != None:
		hdic = anydict(
            "/data1/AD/data/wn17.dict",
            "/data1/AD/data/engdic/", 
            "/data1/AD/data/word.dict"
        )
	else:
		hdic = anydict("C:/Works/ad_svc_backup/ad_svc_data/engdic/")

	hdic.prepare('a', 'a')

	hdic.info()
	#hdic.prn_hdict()
	#hdic.prn_edict()

	#hdic.testit()

	#daemonize()

	main(port)

