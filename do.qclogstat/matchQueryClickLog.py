# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        
# Purpose:
# Author:      daehee00.han
# Created:     25-02-2013
# Copyright:   (c) daehee00.han 2013
import sys
import time
import datetime
import codecs
import handolUtil

def is_non_ascii(ustr):
	for c in ustr:
		v = ord(c)
		if v > 0x7F: return True
	return False
	
def get_qlog_line_dict(fields):
	d = {}
	for fld in fields:
		key,value = fld.split('=', 1)
		value=value.strip()
		if value=='': value="Nil"
		d[key]=value
	return d

def get_time_from_log(fld):
	"""
	QUERY LOG
	25-01-2013 00:00:01:281|ip=|@biz=sa|@shp=722

	CLICK LOG
	25-01-2013 00:00:02:882|test0astorusa01|@-973926579|@
	"""
	try:
		f = fld.split('|')
		t = datetime.datetime.strptime(f[0], "%d-%m-%Y %H:%M:%S:%f")
	except:
		#print "time Error:", fld
		t = None
	return t

class QcLogAnalyzer:
	def __init__(self, myname=''):
		try:
			sys.setdefaultencoding('utf8')
		except:
			import site
			#site.setencoding('utf8')
		self.qcD = {}
		self.langD = handolUtil.AddValueDict("English/Non-English")
		self.imD = handolUtil.AddValueDict("Input Method")
		self.keywordD = handolUtil.AddValueDict("Keywords")
		self.shopkeywordD = handolUtil.AddValueDict("Keyword and Shop")
		self.shopD = handolUtil.AddValueDict("MCC")
		self.osshopD = handolUtil.AddValueDict("OS_MCC")
		self.dosD = handolUtil.AddValueDict("Device OS")
		self.dmD = handolUtil.AddValueDict("Device Model")
		self.devtypeD = handolUtil.AddValueDict("Device Type")
		self.zeroD = handolUtil.AddValueDict("No Res Keywords")
		self.zeroshopkeywordD = handolUtil.AddValueDict("No Res By MCC * Keyword")
		#self.diffsecD = handolUtil.AddValueDict("Seconds to Click")

		self.shopD.set_order('key')
		self.shopkeywordD.set_order('key')
		self.osshopD.set_order('key')
		#self.diffsecD.set_order('key')

		self.cnt_qc_match = 0
		self.cnt_c_only = 0
		self.errcnt_q = 0
		self.errcnt_c = 0
		self.myname = myname

	def test_query_log(self, fname):
		try:
			fp = open(fname, "rb")
			print "Open:", fname
		except:
			return
		loaded = fp.read()
		print "[%d] bytes: %s" % (len(loaded), fname)
		self.query_log_mem(loaded)

	def query_log_mem(self, mem):
		lines = mem.splitlines()
		print "[%d] lines" % len(lines)
		self._query_lines(lines)

	def query_log_file(self, fname):
		try:
			fp = open(fname)
			print "Open:", fname
		except:
			return

		self._query_lines(fp)

	def _query_lines(self, lineiter):
		for i,line in enumerate(lineiter):
			if (i & 0xFFFF) == 1: time.sleep(0.01)
			flds = line.split('|@')
			log_time = get_time_from_log(flds[0])
			d = get_qlog_line_dict(flds[1:])
			res =  self.add_query(d, log_time)
			if res < 0:
				self.errcnt_q += 1

	def add_query(self, q_log_dict, log_time):
		''' return -1 if error found. that means the line is NOT processced.
			return 0 if not processed
			return 1 if processed
		'''
		try:
			im = q_log_dict['im']
		except:
			#print q_log_dict
			return -1

		#if im != 'iqry': return 0
		#if im == 'ac': return 0

		try:
			qh = q_log_dict['qh']
		except:
			#print q_log_dict
			return -1

		if im=='iqry':
			si = q_log_dict.get('si', 'Nil')
			if si!='Nil' and si!='0':
				im='more'

		shop = q_log_dict.get('shp', 'Nil')
		#if shop!="234" and shop!="235" and shop!="450":
		#	return 0

		devtype = q_log_dict.get('dt', 'Nil')
		tot = q_log_dict.get('tot', 'Nil')
		if tot=='Nil': tot = 0
		else: tot = int(tot)
		dos = q_log_dict.get('dos', 'Nil')
		dos = dos.strip()
		if dos!='': dos = dos.split()[0].lower()
		dm = q_log_dict.get('dm', 'Nil')
		dm = "%s_%s" % (dm, dos)
		# value = {query string, im, click cnt, MCC, devtype, tot, click pos, time_diff[]]
		value = [q_log_dict['q'], im, [], shop, devtype, tot, dos, dm, log_time, []]
		self.qcD[qh] = value
		return 1

	def click_log_file(self, fname):
		try:
			fp = open(fname)
			print "Open:", fname
		except:
			return

		self._click_lines(fp)

	def click_log_mem(self, mem):
		lines = mem.splitlines()
		print "[%d] lines" % len(lines)
		self._click_lines(lines)


	def _click_lines(self, lineiter):
		for i,line in enumerate(lineiter):
			if (i & 0xFFFF) == 1: time.sleep(0.01)
			flds = line.split('|@')
			# fld0=time, fld1=qh, fld4=click position, fld5=doc ID
			log_time = get_time_from_log(flds[0])
			if len(flds) != 9:
				self.errcnt_c += 1
				continue
			try:
				self.add_click(flds[1], int(flds[4]), log_time)
			except:
				self.errcnt_c += 1
				#print flds

	def add_click(self, qh, click_pos, c_log_time):
		try:
			value = self.qcD[qh]
			click_list =  value[2]
			q_log_time =  value[8]
			diffsec_list =  value[9]
			click_list.append(click_pos)

			diffsec = handolUtil.timedelta2int(c_log_time - q_log_time)
			diffsec_list.append(diffsec)
			self.cnt_qc_match += 1

		except KeyError:
			#print "query Not Found for", qh
			self.cnt_c_only += 1

	def savefile_qc_matched(self, fname):
		""" store to file
		"""
		print "Save to:", fname
		outf = codecs.open(fname, 'wb', encoding='utf-8')
		for k,v in self.qcD.iteritems():
			keyword = v[0].lower()
			im = v[1]
			clicklist = v[2]
			shop = v[3]
			devtype = v[4]
			tot = v[5]
			dos = v[6]
			dm = v[7]
			diffsec_list =  v[9]
			if len(clicklist)>0:
				anyclick =  1
				click_pos = clicklist[0]
			else:
				anyclick = 0
				click_pos = 0
			line = '%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s\t%s\n' % \
				(im, len(clicklist), click_pos, tot, devtype, dos, dm, shop, keyword)
			outf.write(line)
		outf.close()

	@staticmethod
	def loadfile_qc_matched(fname):
		""" load from a file
		"""
		ecnt=0
		loaded = []
		print "Load from:", fname
		inf = codecs.open(fname, 'rb', encoding='utf-8')
		for line in inf:
			flds = line.split('\t')
			if len(flds) < 8: 
				ecnt += 1
				continue
			flds[-1] = flds[-1].strip()
			loaded.append(flds)
		inf.close()
		print "Good %d, Error %d from %s" % (len(loaded), ecnt, fname)
		return loaded
		
	def get_stats_from_qcmatched(self, fname):
		""" calculate statistics from Query/Click matched log
		"""
		stopwatch = handolUtil.StopWatch()
		stopwatch.start()
		qcmatched_list = QcLogAnalyzer.loadfile_qc_matched(fname)
		print "Loading : %f sec" % (stopwatch.laptime())
		stopwatch.start()
		
		for v in qcmatched_list:			
			im = v[0]
			num_clicks = int(v[1])
			click_pos = int(v[2])
			tot = int(v[3])
			devtype = v[4]
			dos = v[5]
			dm = v[6]
			shop = v[7]
			keyword = v[8]
			if tot==0: nores = 1
			else: nores = 0
			if num_clicks>0:
				anyclick =  1	
			else:
				anyclick = 0
			
			if is_non_ascii(keyword):
				english = 0
			else:
				english = 1
				
			os_shop = "%s_%s" % (dos, shop)
			shop_keyw = (shop, keyword)
			self.langD.add(english, [1, anyclick, nores, click_pos, num_clicks])
			self.imD.add(im, [1, anyclick, nores, click_pos, num_clicks, english]) # query count, click
			self.keywordD.add(keyword, [1, anyclick, nores, click_pos, num_clicks, english])
			self.shopkeywordD.add(shop_keyw, [1, anyclick, nores, click_pos, num_clicks])
			self.shopD.add(shop, [1, anyclick, nores, click_pos, num_clicks, english])
			self.osshopD.add(os_shop, [1, anyclick, nores, click_pos, num_clicks, english])
			self.devtypeD.add(devtype, [1, anyclick, nores, click_pos, num_clicks, english])
			self.dosD.add(dos, [1, anyclick, nores, click_pos, num_clicks, english])
			self.dmD.add(dm, [1, anyclick, nores, click_pos, num_clicks, english])
			#self.diffsecD.add(diffsec, [1, anyclick, nores, click_pos, len(clicklist)])

			if tot==0:
				self.zeroD.add(keyword, [1, english])
				#self.zeroshopD.add(shop, [1])
				#self.zeroshopkeywordD.add(shop_keyw, [1])
				
		print "Calculating : %f sec" % (stopwatch.laptime())
		
	def get_stats(self, fname):
		""" calculate statistics from Query/Click matched log
		"""
		for k,v in self.qcD.iteritems():
			keyword = v[0].lower()
			im = v[1]
			clicklist = v[2]
			shop = v[3]
			devtype = v[4]
			tot = v[5]
			dos = v[6]
			dm = v[7]
			diffsec_list =  v[9]

			if len(diffsec_list)>0: diffsec = diffsec_list[0]
			else: diffsec = -1

			if diffsec > 60*5: diffsec = 60*5
			if diffsec < -1: diffsec = -2

			if len(clicklist)>0:
				anyclick =  1
				click_pos = clicklist[0]

			else:
				anyclick = 0
				click_pos = 0

			if tot==0: nores = 1
			else: nores = 0

			os_shop = "%s_%s" % (dos, shop)
			shop_keyw = (shop, keyword)
			self.imD.add(im, [1, anyclick, nores, click_pos, len(clicklist) ]) # query count, click
			self.keywordD.add(keyword, [1, anyclick, nores, click_pos, len(clicklist) ])
			self.shopkeywordD.add(shop_keyw, [1, anyclick, nores, click_pos, len(clicklist)])
			self.shopD.add(shop, [1, anyclick, nores, click_pos, len(clicklist)])
			self.osshopD.add(os_shop, [1, anyclick, nores, click_pos, len(clicklist)])
			self.devtypeD.add(devtype, [1, anyclick, nores, click_pos, len(clicklist)])
			self.dosD.add(dos, [1, anyclick, nores, click_pos, len(clicklist)])
			self.dmD.add(dm, [1, anyclick, nores, click_pos, len(clicklist)])
			#self.diffsecD.add(diffsec, [1, anyclick, nores, click_pos, len(clicklist)])

			if tot==0:
				self.zeroD.add(keyword, [1])
				#self.zeroshopD.add(shop, [1])
				#self.zeroshopkeywordD.add(shop_keyw, [1])

	def print_stats(self, outf=''):
		"""
		print out result.
		if outf is given, stdout is redirected to the file 'outf'
		"""
		if outf != '':
			backup = sys.stdout
			sys.stdout = codecs.open(outf, 'wb', encoding='utf-8')

		print "##########"
		print "LOGNAME ,", self.myname

		print "self.errcnt_q ,", self.errcnt_q
		print "self.errcnt_c ,", self.errcnt_c
		print "self.cnt_qc_match ,", self.cnt_qc_match
		print "self.cnt_c_only ,", self.cnt_c_only

		print "keywords(all) , ", len(self.keywordD)
		print "searches(top 100) , ", self.keywordD.sum_of_tops(100)
		print "searches(top 200) , ", self.keywordD.sum_of_tops(200)
		print "searches(top 300) , ", self.keywordD.sum_of_tops(300)
		print "searches(top 1000) , ", self.keywordD.sum_of_tops(1000)
		print "searches(top 1500) , ", self.keywordD.sum_of_tops(1500)

		print "keywords(no result) , ", len(self.zeroD)
		print "searches(top 10 keywords with no result) , ", self.zeroD.sum_of_tops(10)
		print "searches(top 50 keywords with no result) , ", self.zeroD.sum_of_tops(50)
		print "searches(top 100 keywords with no result) , ", self.zeroD.sum_of_tops(100)
		print "searches(keywords with no result) , ", self.zeroD.sum_of_tops()

		print
		print "########## Click Ratio by Language"	
		self.langD.prn()
		print
		print "########## Click Ratio by Device Type"
		self.devtypeD.prn()

		print "########## Click Ratio by IM(Input Method)"
		self.imD.prn()

		print "########## Click Ratio by Device OS"
		self.dosD.prn()

		print "########## Click Ratio by MCC"
		self.shopD.prn()

		print "########## Click Ratio by MCC and OS"
		self.osshopD.prn()


		print "########## Click Ratio by Device Model"
		self.dmD.prn()

		print "########## Click Ratio by Seconds-to-Click"
		#self.diffsecD.prn()

		print "########## Top 1500 the Keywords (order by frequency)"
		self.keywordD.prn(1000)

		print "########## Keyword with NO results (order by frequency"
		self.zeroD.prn(1000)

		sys.stdout.close()
		if outf != '':
			sys.stdout = backup





def save_qcmatched(org_log_dir, daystr):
	os.chdir(org_log_dir)	
	print "DIR:", os.getcwd()	
	print "DAY:", daystr
	QUERY_FILES = [
		'euospcomp07.osp_query.log',
		'euospcomp08.osp_query.log',
		'euospsch01.osp_query.log',
		'euospsch03.osp_query.log',
		'euospsch01.2.osp_query.log',
		'euospsch03.2.osp_query.log',
		'cnosptrs01.osp_query.log',
		'cnosptrs02.osp_query.log'		
	]

	CLICK_FILES = [
		'euospsch03.osp_click.log',
		'euospcomp08.osp_click.log',
		'cnosptrs01.osp_click.log',
		'cnosptrs02.osp_click.log'
	]

	#QUERY_FILES = QUERY_FILES[:1]
	#CLICK_FILES = CLICK_FILES[:1]



	analyzer = QcLogAnalyzer(daystr)

	#analyzer.query_log_file("a.query.log")
	#analyzer.click_log_file("a.click.log")

	
	for f in QUERY_FILES:
		qfile = "%s.%s" % (f, daystr)
		analyzer.query_log_file(qfile)
		sys.stdout.flush()

	for f in CLICK_FILES:
		cfile = "%s.%s" % (f, daystr)
		analyzer.click_log_file(cfile)
		sys.stdout.flush()
		
	QCLOG = "qc_matched.all.%s.log" % daystr
	analyzer.savefile_qc_matched(QCLOG)

def load_qcmatched(org_log_dir,daystr):
	os.chdir(org_log_dir)	
	print "DIR:", os.getcwd()	
	print "DAY:", daystr
	
	stopwatch = handolUtil.StopWatch()
	stopwatch.start()
	analyzer = QcLogAnalyzer(daystr)
	QCLOG = "qc_matched.all.%s.log" % daystr
	analyzer.get_stats_from_qcmatched(QCLOG)
	print "Loading & Statistics: %f sec" % (stopwatch.laptime())
	
	stopwatch.start()
	analyzer.print_stats('%s.all.csv' % (daystr))
	print "Saving output: %f sec" % (stopwatch.laptime())
	
	#analyzer.print_info('%s.csv' % (daystr))
	#analyzer.save_to_mongo()
	#analyzer.save_keywords()
	
if __name__=="__main__":
	import os
	import sys	
	#os.chdir(sys.argv[1])
	#daystr = sys.argv[2]
	org_log_dir = u"D:/0001/9 org logs/20130215"
	daystr = '20130215'
	stopwatch = handolUtil.StopWatch()
	stopwatch.start()
	#save_qcmatched(org_log_dir, daystr)
	load_qcmatched(org_log_dir, daystr)
	print is_non_ascii('avcd')
	print is_non_ascii('微信')
	