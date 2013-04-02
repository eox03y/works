from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key
import os.path
import handolUtil

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

def get_file_to_mem(conn, b_name, k_name):
	b = conn.get_bucket(b_name)
	k = b.lookup(k_name)
	content = k.get_contents_as_string()
	return k.size, content	

def get_file_to_mem(conn, b_name, k_name):
	b = conn.get_bucket(b_name)
	k = b.lookup(k_name)
	if k == None:
		return 0, ''
	content = k.get_contents_as_string()
	return k.size, content	



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
	rs = b.get_all_keys(prefix=prefix_s, max_keys=100)
	#print '# of ResultSet =', rs.size()
	for k in rs:
		print "%s [%d]" %(k.name, k.size)
	
def download_files(conn, b_name, prefix_s):
	b = conn.get_bucket(b_name)
	rs = b.get_all_keys(prefix=prefix_s, max_keys=100)
	print '# of ResultSet =', len(rs)
	for k in rs:
		print "Info: size=%d Kb, type=%s" %( int(k.size/1024), k.content_type)
		prompt="Download %s" %(k.name)
		res = handolUtil.y_or_n(prompt)
		if res:
			simple_name = os.path.basename(k.name)
			k.get_contents_to_filename(simple_name)
			print "----> %s" % (simple_name)
	

	
AWS_ACCESS_KEY_ID = 'AKIAILHNCYCVT6OGN5JA'
AWS_SECRET_ACCESS_KEY = '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'
conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)



import sys
if __name__=="__main__":
	if len(sys.argv) < 0: 
		print "Usage: source(local) target(s3)"
		sys.exit()

	#list_files2(conn, 'sch-emr', 'DEVELOPING/app/7nmc1m75ij/apps-log/query_log/20130125/')
	#list_files2(conn, 'sch-emr', 'DEVELOPING/app/7nmc1m75ij/apps-log/query_log/')
	org_size, loaded_mem = get_file_to_mem(conn, 'sch-emr', 'DEVELOPING/app/7nmc1m75ij/apps-log/click_log/20130125/euospsch03.osp_click.log.20130125')
	print "ORG [%d] LOAD [%d]" % (org_size, len(loaded_mem))
	if org_size != len(loaded_mem):
		print "!!! NOT fully loaded"
	#download_files(conn, 'sch-emr', 'DEVELOPING/app/7nmc1m75ij/apps-log/query_log/20130125/')

