import sys
import time
import datetime
def get_qlog_line_dict(fields):
	resD = {}
	for fld in fields:
		key,value = fld.split('=', 1)
		resD[key]=value
	return resD
	 

class LogAnalyzer:
	def __init__(self):
		self.D = {}
		self.cnt_qh = 0
	
	def query_log(self, fname):
		fp = open(fname)
		print "Open:", fname
		for i,line in enumerate(fp):
			if (i & 0x7FFF) == 1: time.sleep(0.01)
			flds = line.split('|@')
			d = get_qlog_line_dict(flds[1:])
			res =  self.add_query(d)	
	
	def add_query(self, q_log_dict):
		''' return -1 if error found. that means the line is NOT processced.
		    return 0 if not processed
		    return 1 if processed 
		'''
		try:
			im = q_log_dict['im']
		except:
			print q_log_dict
			return -1

		#if im != 'iqry': return 0
		if im == 'ac': return 0
		
		try:
			qh = q_log_dict['qh']
		except:
			qh = None
		if qh==None: 
			print q_log_dict
			return -1

		value = [q_log_dict['q'], q_log_dict['biz'], None]
		self.D[qh] = value
		return 1

	def click_log(self, fname):
		fp = open(fname)
		print "Open:", fname
		for i,line in enumerate(fp):
			if (i & 0x7FFF) == 1: time.sleep(0.01)
			flds = line.split('|@')
			# fld0=time, fld1=qh, fld5=doc ID
			if len(flds) < 6: continue
			self.add_click(flds[1], flds[5])

	def add_click(self, qh, docid):
		try:
			value = self.D[qh]
			value[2] = docid
			
		except:
			self.cnt_qh += 1
			#print "query Not Found for", qh

	def print_info(self):
		cnt = 0
		for k,v in self.D.iteritems():
			print k, v
			cnt += 1	
			if cnt > 10: break

	def get_rate(self):
		cnt = 0
		for k,v in self.D.iteritems():
			if v[2] != None: cnt += 1	
		print "Total=%d, Hit=%d, Ratio=%f" % (len(self.D), cnt, (cnt/len(self.D)*100.0))
		print "self.cnt_qh", self.cnt_qh

if __name__=="__main__":
	analyzer = LogAnalyzer()
	analyzer.query_log('euospcomp07.osp_query.log.20130125')
	analyzer.query_log('euospcomp08.osp_query.log.20130125')
	analyzer.query_log('euospsch01.osp_query.log.20130125')
	analyzer.query_log('euospsch03.osp_query.log.20130125')
	analyzer.query_log('euospsch01.2.osp_query.log.20130125')
	analyzer.query_log('euospsch03.2.osp_query.log.20130125')
	analyzer.click_log('euospsch03.osp_click.log.20130125')
	analyzer.click_log('euospcomp08.osp_click.log.20130125')
	analyzer.print_info()
	analyzer.get_rate()
