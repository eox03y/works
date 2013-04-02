from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key

def list_buckets(conn):
	rs = conn.get_all_buckets()
	print "== buckets (%d) ==" % (len(rs))
	for b in rs:
		print b.name
	#print dir(rs[0])

def search_bucket(conn, b_name):
	b = conn.get_bucket(b_name)
	print b
	k = Key(b)	
	print k, k.name, k.metadata	

def search_file(conn, b_name, k_name):
	b = conn.get_bucket(b_name)
	k = b.lookup(k_name)
	print k

def get_file(conn, b_name, k_name):
	b = conn.get_bucket(b_name)
	k = b.lookup(k_name)
	k.get_contents_to_filename(k_name)
	content = k.get_contents_as_string()
	print "==", k_name, len(content)

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


import sys
if __name__=="__main__":
	if len(sys.argv) < 3: 
		print "Usage: source(local) target(s3)"
		sys.exit()

	put_file(conn, 'sch-emr', sys.argv[1], sys.argv[2])

