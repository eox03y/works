# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        qcmerger
# Purpose:
#
# Author:      daehee00.han
#
# Created:     2013/05/10
# Copyright:   (c) daehee00.han 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import sys
import re
import codecs
import operator
from operator import itemgetter
import handolUtil
import handolS3Util

MAPPER_SHOPID_APPS = {
	"450":"KOR", "234":"GBR", "235":"GBR"
}
MAPPER_SHOPID_LHRHVH = {
	"GLH" : { "1":"KOR", "3":"GBR" },
	"GRH" : { "24":"KOR", "26":"GBR" },
	"GVH" : { "1007":"KOR", "1006":"GBR" }
}

"""
'euospcomp07.osp_query.log',
		'euospcomp08.osp_query.log',
		'euospsch01.osp_query.log',
		'euospsch03.osp_query.log',
		'euospsch01.2.osp_query.log',
		'euospsch03.2.osp_query.log'
		'euospsch03.osp_click.log',
		'euospcomp08.osp_click.log'
config file in JSON format:
value of 'FROM': S3 or local
{ 
   "FROM": "S3",
   "QUERY FILES": 
   [  
   "DEVELOPING/app/7nmc1m75ij/apps-log/query_log/YYYYMMDD/euospcomp07.osp_query.log.YYYYMMDD",
   "DEVELOPING/app/7nmc1m75ij/apps-log/query_log/YYYYMMDD/euospcomp08.osp_query.log.YYYYMMDD",
   ],
   
   "CLICK FILES": 
   [  
   "DEVELOPING/app/7nmc1m75ij/apps-log/query_log/YYYYMMDD/euospsch03.osp_click.log.YYYYMMDD",
   "DEVELOPING/app/7nmc1m75ij/apps-log/query_log/YYYYMMDD/euospcomp08.osp_click.log.YYYYMMDD",
   ]
 }
"""
def load_jsonfile(fname):
	if fname=='-':        
		fp = codecs.getreader('utf-8')(sys.stdin)
	else:
		fp = codecs.open(fname, 'rb', encoding='utf-8')
	lines  = fp.read()
	fp.close()

	jdata = json.loads(lines)
	return jdata

def set_date_in_fname(fname, yyyymmdd):
	fname = fname.replace('YYYY', yyyymmdd[:4])
	fname = fname.replace('MM', yyyymmdd[4:6])
	fname = fname.replace('DD', yyyymmdd[6:8])
	return fname

"""
load config file and check it
"""
CFG_KEYS = ["FROM", "SVC", "QUERY FILES", "CLICK FILES"]
def load_config_json(fname, yyyymmdd):
	cfg = load_jsonfile(fname)
	for key in CFG_KEYS:
		if not cfg.has_key(key):
			print "key '%s' missing in config file '%s'" % (key, fname)
			return None
			
	cfg["QUERY FILES"] = map(lambda x: set_date_in_fname(x, yyyymmdd), cfg["QUERY FILES"])	
	cfg["CLICK FILES"] = map(lambda x: set_date_in_fname(x, yyyymmdd), cfg["CLICK FILES"])
	
	return cfg
	
"""
"""	
def is_non_ascii(ustr):
	for c in ustr:
		v = ord(c)
		if v > 0x7F: return True
	return False

"""
25-01-2013 00:00:01:281|ip=|@biz=sa|@shp=722
"""
def get_time_from_log(fld):
	try:
		f = fld.split('|')
		t = datetime.datetime.strptime(f[0], "%d-%m-%Y %H:%M:%S:%f")
	except:
		#print "time Error:", fld
		t = None
	return t
	
	
"""
"""
def line_yield(mem_lines):
	for line in mem_lines.splitlines():
		line = unicode(line, encoding='utf-8')
		yield line

"""
"""
def load_from_s3(bucket, s3file):
	org_size, mem = handolS3Util.get_file_to_mem( handolS3Util.conn, bucket, s3file)
	print "Open S3: %s/%s" % (bucket, s3file)
	print "ORG [%d] LOAD [%d]" % (org_size, len(mem))
	if org_size==0 or org_size != len(mem):
		print "Failed:", s3file
		return None
	else:
		return mem

"""
Iterator over a file or a large memory of string
"""
#from cStringIO import StringIO
from StringIO import StringIO
def iter_line_S3(bucket, s3file):		
	mem = load_from_s3(bucket, s3file)
	if mem:
		return StringIO(unicode(mem, encoding='utf-8'))
		#return StringIO(mem)
	else: 
		return None

"""
Iterator over a file
"""
def iter_line_file(fname):
	try:
		fp = codecs.open(fname, 'rb', encoding='utf-8')
		print "Open:", fname
	except:
		print "Open Failed:", fname
		return None
	return fp


"""
"""
def get_keyvalue_from_logline(fields):
	d = {}
	for fld in fields:
		try:
			key,value = fld.split('=', 1)
		except:
			return None
		value=value.strip()
		if value=='': value="nil"
		d[key]=value
	return d


"""
Parse SAMSUNG APPS click log
"""
def filer_for_APPS_click(line):	
	flds = line.split('|@')
	# fld0=time, fld1=qh, fld4=click position, fld5=doc ID
	if len(flds) != 9: 
		return None
	qh = flds[1]
	idx = flds[4]
	return [qh, idx]	

"""
Parse SAMSUNG APPS query log
"""
def filer_for_APPS_query(line):
	''' input: line of SamsungApps query log
		output: list of fields
	'''
	flds = line.split('|@')
	d = get_keyvalue_from_logline(flds[1:])
	if d==None: return None
	
	qh = d.get('qh', None)	
	q = d.get('q', None)
	if qh==None or q==None: return None
	
	dt = d.get('dt', 'null')
	dos = d.get('dos', 'null')
	im = d.get('im', 'null')	
	shp = d.get('shp', None)	
	
	if im=='iqry':
		si = d.get('si', None)
		if si!=None and si!='0':
			im='more'
	
	tot = d.get('tot', '0')	
	return [qh, dt, dos, im, shp, q, tot]	

"""
Parse SAMSUNG HUB click log

07-05-2013 00:24:01:607||@sn=GLH|@qh=136373520|@qid=GLH.SRCH.SCORE|@q=jerman|@tot=1|@idx=0|@doc=35|30110235|@title=Belajar+Bahasa+Jerman+Kamus+Visual|Belajar+Bahasa+Jerman+Kamus+Visual
"""
def filer_for_HUB_click(line):
	flds = line.split('|@')
	d = get_keyvalue_from_logline(flds[1:])
	if d==None: return None	

	qh = d.get('qh', None) # query hash code	
	if qh==None: 
		print "!! QH missing"
		print line
		return None

	idx = d.get('idx', '0')
	svc = d.get('sn', None)	 # LH, RH, VH, ...
	return [qh, idx, svc]	

"""
Parse SAMSUNG HUB query log line

09-05-2013 13:21:10:899|@ctry=nil|@dt=phone|@dm=GT-I9505|@dos=17|@did=jI+jNi+BHXMhL7Lbhg4UDA|@ip=192.168.0.155|@im=iqry|@q=zxcvbn1|@n=20|@si=0|@biz=glh|@shp=nil|@qv=pd|@qid=GLH.SRCH.SCORE|@sn=GLH|@qh=1715063252|@tot=0|@sts=0|@set=84|@pet=102|@tet=102|@shop=0
"""
def filer_for_HUB_query(line):
	flds = line.split('|@')
	d = get_keyvalue_from_logline(flds[1:])
	if d==None: return None
	
	qh = d.get('qh', None)	
	q = d.get('q', None)
	qid = d.get('qid', None)
	if qh==None or q==None or qid==None: return None
	
	# filter out 'auto complete' request
	if d['qid'][0]=='_' or d['qid'].find('.AUT') != -1:
		return None
	
	#ctry = d['ctry']
	dt = d.get('dt', 'null')
	dos = d.get('dos', 'null')
	im = d.get('im', 'null')
	svc = d.get('sn', 'null')
	shp = d.get('shop', None)
	if not shp: shp = d.get('shp', None)
	if not shp: shp = 'null'

	if im=='iqry':
		si = d.get('si', None)
		if si!=None and si!='0':
			im='more'			
	
	tot = d.get('tot', '0')		

	return [qh, dt, dos, im, shp, q, tot, svc]	
	

###
"""
1) load all click log files into memory
2) load one query log file into memory
3) write matching result of one query file to a output file, and then flush
4) loop step2
"""
class QueryClickMatcher:
	def __init__(self, svcname, myname):
		'''
		svcname must be one of "HUB", "APPS".
		'''
		self.SVC = svcname
		self.myname = myname
		self.errcnt_q = 0
		self.errcnt_c = 0
		self.srcList = []
		self.fileList = {}
		self.clickD = {} # Dict of click info
		
	def add_click_file(self,  fname, bucket=None):
		if bucket:	lineiter = iter_line_S3(bucket, fname)
		else:		lineiter = iter_line_file(fname)	

		if self.SVC=="APPS":	filter_func = filer_for_APPS_click
		elif self.SVC=="HUB":	filter_func = filer_for_HUB_click
		else:					return 0
		
		# this is more 'Pythonic',  oneList - result from one file
		#oneList = [flds for flds in [filter_func(line) for line in lineiter] if flds]		
		cnt = 0
		for line in lineiter:
			flds = filter_func(line)
			if not flds: continue
			# qh == flds[0]
			self.clickD[flds[0]] = flds[1:]
			cnt += 1
			
		self.fileList[fname] = cnt
		return 
		
	def add_query_file(self,  fname, bucket=None):
		if bucket:	lineiter = iter_line_S3(bucket, fname)
		else:		lineiter = iter_line_file(fname)	

		if self.SVC=="APPS":	filter_func = filer_for_APPS_query
		elif self.SVC=="HUB":	filter_func = filer_for_HUB_query
		else:					return 0
		
		qclist = []		
		for line in lineiter:
			flds = filter_func(line)
			if not flds: continue
			
			# qh == flds[0]
			cinfo = self.clickD.get(flds[0], None)
			# chk svc name
			if cinfo and cinfo[1]==flds[-1]:
				flds.append(cinfo[0])
			else:
				pass
			qclist.append(flds)		
		
		return qclist

	@staticmethod	
	def save_qc_match(qclist, outfile):
		""" store to files.  one file for each service (LH, RH, VH)	
			
		"""
		outfdDict = {}
		print "Save to:", outfile
		for qc in qclist:			
			line = '\t'.join(qc) # delimiter is 'tab' character.
			svc = qc[7]
			
			outf = outfdDict.get(svc, None)
			if not outf:
				outfname = outfile + '.' + svc
				outf = codecs.open(outfname, 'wb', encoding='utf-8')
				outfdDict[svc] = outf
			outf.write(line + '\n')
			
		for outf in outfdDict.itervalues():
			outf.close()

	@staticmethod
	def load_qc_match(fname):
		""" load from a file
		"""		
		loaded = []
		print "Load from:", fname
		inf = codecs.open(fname, 'rb', encoding='utf-8')
		for line in inf:
			flds = line.split('\t')			
			flds[-1] = flds[-1].lstrip()
			loaded.append(flds)
		inf.close()
		print "Good %d from %s" % (len(loaded), fname)
		return loaded
		
	#			
	def main(self, bucket, cfiles, qfiles, outfile):	
		stopwatch = handolUtil.StopWatch()
		for cfile in cfiles:
			self.add_click_file(cfile, bucket)
			print "Loading Click - %s: %f sec" % (cfile, stopwatch.laptime())
		
		qclistAll = []
		for qfile in qfiles:
			qclist = self.add_query_file(qfile, bucket)
			qclistAll += qclist
			print "Load Query & Match - %s: %f sec" % (qfile, stopwatch.laptime())
		
		QueryClickMatcher.save_qc_match(qclistAll, outfile)	
		#	handolS3Util.put_file( handolS3Util.conn, bucket, outfile, 'handol/%s' % outfile)

###
"""
"""
class QueryClickStat:		
	#
	def __init__(self, svcname='', myname=''):
		'''
		svcname must be one of "HUB", "APPS".
		'''
		self.SVC = svcname
		self.myname = myname
		self.FLD_NAMES = ['dt', 'dos', 'im', 'shp'] 
		self.statD = [None] * len(self.FLD_NAMES)
		for i,fld in enumerate(self.FLD_NAMES):
			self.statD[i] = handolUtil.AddValueDict(fld)	

	'''
	read matchfile,
	wrtie statfile
	'''
	def main(self, matchfile, statfile):
		qclist = QueryClickMatcher.load_qc_match(matchfile)	
		self.get_stats(qclist)
		
	def get_stats(self, qclist):
		""" calculate statistics and store into self.statD
		
		qclist:
		[qh, dt, dos, im, shp, q, tot, svc]		
		[qh, dt, dos, im, shp, q, tot, svc, idx]		
		"""		
		for v in qclist:		
			tot = int(v[6])
			if tot==0: nores = 1
			else: nores = 0		
			
			if len(v)>8:
				anyclick =  1
				click_pos = int(v[8])
			else:
				anyclick = 0
				click_pos = 0
				
			for i,fld in enumerate(self.FLD_NAMES):
				self.statD[i].add(v[i+1], [1, anyclick, nores, click_pos])
		
		for i,fld in enumerate(self.FLD_NAMES):
				self.statD[i].prn()		
					

if __name__=="__main__":
	if len(sys.argv) < 3 or sys.argv[1][0]!='-':
		print "Usage: -match yyyymmdd config_file match_file"
		print "Usage: -stat match_file "
		sys.exit()
	
	act = sys.argv[1][1:]	
	yyyymmdd = sys.argv[2]
	
	if act=='match':
		cfgfile = sys.argv[3]
		matchfile = sys.argv[4]
		
		cfg = load_config_json(cfgfile, yyyymmdd)
		if  not cfg: 
			sys.exit()
			
		qcmatcher = QueryClickMatcher(cfg["SVC"], yyyymmdd)
		qcmatcher.main(  cfg.get("BUCKET", None), cfg["CLICK FILES"], cfg["QUERY FILES"], matchfile )
	else:
		matchfile = sys.argv[2]
		#statfile = sys.argv[3]
		stat = QueryClickStat()
		stat.main(matchfile, None) 
		
