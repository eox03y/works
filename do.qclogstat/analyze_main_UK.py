import sys
import time
import datetime
import handolS3Util
import handolUtil
import queryClickLogUKKOR as queryClickLog

QUERY_FILES = [
	'euospcomp07.osp_query.log',
	'euospcomp08.osp_query.log',
	'euospsch01.osp_query.log',
	'euospsch03.osp_query.log',
	'euospsch01.2.osp_query.log',
	'euospsch03.2.osp_query.log',
]

CLICK_FILES = [
	'euospsch03.osp_click.log',
	'euospcomp08.osp_click.log'
]

S3_DIR_QUERY = "DEVELOPING/app/7nmc1m75ij/apps-log/query_log/"
S3_DIR_CLICK = "DEVELOPING/app/7nmc1m75ij/apps-log/click_log/"
BUCKET = "sch-emr"

def make_q_names(datestr):
	res = []
	for f in QUERY_FILES:
		s3_name = "%s%s/%s.%s" % (S3_DIR_QUERY, datestr, f, datestr)
		res.append(s3_name)
	return res

def make_c_names(datestr):
	res = []
	for f in CLICK_FILES:
		s3_name = "%s%s/%s.%s" % (S3_DIR_CLICK, datestr, f, datestr)
		res.append(s3_name)
	return res

def analyze_oneday_log_file(daystr, outf=''):
	analyzer = queryClickLog.LogAnalyzer()

	for f in QUERY_FILES:
		qfile = "%s.%s" % (f, daystr)
		analyzer.query_log_file(qfile)
		sys.stdout.flush()

	for f in CLICK_FILES:
		cfile = "%s.%s" % (f, daystr)
		analyzer.click_log_file(cfile)
		sys.stdout.flush()
	analyzer.get_rate()
	#analyzer.print_info(outf)
	analyzer.save_to_mongo()
	analyzer.save_keywords()

def analyze_oneday_log_s3(daystr, outf=''):
	analyzer = queryClickLog.LogAnalyzer(daystr)

	for qfile in make_q_names(daystr):
		print qfile
		org_size, mem = handolS3Util.get_file_to_mem( handolS3Util.conn, BUCKET, qfile)
		print "ORG [%d] LOAD [%d]" % (org_size, len(mem))
		if org_size==0 or org_size != len(mem):
			print "!!! NOT fully loaded"
			continue
		analyzer.query_log_mem(mem)
		sys.stdout.flush()

	for cfile in make_c_names(daystr):
		print cfile
		org_size, mem = handolS3Util.get_file_to_mem( handolS3Util.conn, BUCKET, cfile)
		print "ORG [%d] LOAD [%d]" % (org_size, len(mem))
		if org_size==0 or org_size != len(mem):
			print "!!! NOT fully loaded"
			continue
		analyzer.click_log_mem(mem)
		sys.stdout.flush()

	analyzer.get_rate()
	#analyzer.print_info(outf)
	analyzer.save_to_mongo()
	analyzer.save_keywords()


######
if __name__=="__main__":
#	print make_q_names('20130110')
#	print make_c_names('20130110')

	if len(sys.argv) < 3:
		print "usage: start_day end_day"
		print "usage: 2011-10-7 2011-10-13"
		sys.exit()

	daylist = handolUtil.get_day_list(sys.argv[1],sys.argv[2])
	
	for daystr in daylist:
		print datetime.datetime.now()
		outf = "qc_log.%s.csv" % (daystr)
		print "### PROCESSING - %s" % (daystr)
		try:
			analyze_oneday_log_s3(daystr, outf )
		except:
			print "FAILED - %s" % (daystr)
			if daystr==daylist[-1]: raise
			
			

