from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key
import time
import os
import sys

def get_file(conn, b_name, k_name):
	b = conn.get_bucket(b_name)
	k = b.lookup(k_name)
	k.get_contents_to_filename(k_name)
	content = k.get_contents_as_string()
	print "==", k_name, len(content)

def get_filesize(conn, b_name, k_name):
	b = conn.get_bucket(b_name)
	k = b.lookup(k_name)
	if k==None: return 0
	else: return k.size

def put_file(conn, b_name, src_file, remote_file):
	b = conn.get_bucket(b_name)
	k = Key(b)
	k.key = remote_file
	k.set_contents_from_filename(src_file)

	
def list_files(conn, b_name, prefix_s):
	b = conn.get_bucket(b_name)
	rs = b.list(prefix=prefix_s)
	#print '# of ResultSet =', rs.size()
	for k in rs:
		print k.name

def list_files2(conn, b_name, prefix_s):
	b = conn.get_bucket(b_name)
	rs = b.get_all_keys(prefix=prefix_s, max_keys=3)
	#print '# of ResultSet =', rs.size()
	for k in rs:
		print k.name
	

	
AWS_ACCESS_KEY_ID = 'AKIAILHNCYCVT6OGN5JA'
AWS_SECRET_ACCESS_KEY = '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'


conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

S3ADDR = [ \
 'DEVELOPING/app/7nmc1m75ij/apps-log/query_log/YYYYMMDD/$HOST1.osp_query.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/apps-log/click_log/YYYYMMDD/$HOST2.osp_click.log.YYYYMMDD',	
 'DEVELOPING/app/7nmc1m75ij/uscloud1/query_log/osp_Predefined-Query.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/uscloud2/query_log/osp_Predefined-Query.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/uscloud3/query_log/osp_Predefined-Query.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/uscloud1/click_log/iosp_click.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/uscloud2/click_log/iosp_click.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/uscloud3/click_log/iosp_click.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/eucloud1/query_log/osp_Predefined-Query.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/eucloud2/query_log/osp_Predefined-Query.log.YYYYMMDD',
 'DEVELOPING/app/7nmc1m75ij/eucloud3/query_log/osp_Predefined-Query.log.YYYYMMDD',
# 'DEVELOPING/app/7nmc1m75ij/eucloud1/click_log/iosp_click.log.YYYYMMDD',
# 'DEVELOPING/app/7nmc1m75ij/eucloud2/click_log/iosp_click.log.YYYYMMDD',
# 'DEVELOPING/app/7nmc1m75ij/eucloud3/click_log/iosp_click.log.YYYYMMDD'
]

HOST1 = ['euospsch01', 'euospsch01.2', 'euospsch03', 'euospsch03.2', 'euospcomp07', 'euospcomp08', 'cnosptrs01', 'cnosptrs02']
HOST2 = ['euospsch03', 'euospcomp08', 'cnosptrs01', 'cnosptrs02']

def check_files(yymmdd, out=sys.stdout):
	for ptn in S3ADDR:
		if '$HOST1' in ptn:
			files  = [ptn.replace('$HOST1', h) for h in HOST1]
		elif '$HOST2' in ptn:
			files  = [ptn.replace('$HOST2', h) for h in HOST2]
		else:
			files = [ptn]

		files = [f.replace('YYYYMMDD', yymmdd) for f in files]
		for f in files:
			s3fsize = get_filesize(conn, 'sch-emr', f)
			if s3fsize:
				msg = "OK"
			else:
				msg = "MISS"
			out.write("%s\t%s\t%.1f Mb\n" % (msg, f, s3fsize/(1024*1024.0)))
		
	

import boto.ses

FROM_ADDR = 'hjguy.han@samsung.com'
FROM_ADDR = 'daehee00.han@samsung.com'
TO_ADDR = [
#'hseok7.shim@samsung.com',
#'hjguy.han@samsung.com',
'sukhoo.hong@samsung.com',
'yc1599.choi@samsung.com',
'muse.kang@samsung.com',
'jungwa.lee@partner.samsung.com',
#'jy7340.jung@samsung.com',
#'shawn.s.park@samsung.com',
'daehee00.han@samsung.com'
]



def send_email(yymmdd, content):
	'''
	conn = boto.ses.connect_to_region(
		'us-east-1',
		#'us-west-2',
		aws_access_key_id=AWS_KEY,
		aws_secret_access_key=ACCESS_KEY
		)
	'''
	AWS_ACCESS_KEY_ID='AKIAJT7UGP5BJCIT7QZQ',
	AWS_SECRET_ACCESS_KEY='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'
	conn = boto.ses.SESConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

	#senders = conn.list_verified_email_addresses()
	#senders = filter(lambda e: not e.find('samsung.com')==-1, senders)
	#print senders

	if content.find('MISS') != -1:
		ok = 'Missing'
	else:
		ok = 'OK'
	title = '[SSP Search Log %s] %s' % (yymmdd, ok)
	try:
		res = conn.send_email(source=FROM_ADDR,  subject=title,
			body=content, to_addresses=TO_ADDR,
			bcc_addresses=None, format='text', reply_addresses=[FROM_ADDR], return_path=None)
		#print res
		print 'email sent'
	except Exception, e:
		print e



import sys
if __name__=="__main__":
	if len(sys.argv) < 2: 
		print "Usage: YYYYMMDD MAIL"
		sys.exit()

	#put_file(conn, 'sch-emr', sys.argv[1], sys.argv[2])

	from StringIO import StringIO
	out = StringIO()
	check_files(sys.argv[1], out)

	if len(sys.argv)>2 and sys.argv[2]=='MAIL':
		send_email(sys.argv[1], out.getvalue())
	else:
		print out.getvalue()	
