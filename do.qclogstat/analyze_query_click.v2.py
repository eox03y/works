import sys
import time
import datetime
from operator import itemgetter


def get_qlog_line_dict(fields):
	resD = {}
	for fld in fields:
		key,value = fld.split('=', 1)
		resD[key]=value
	return resD
	 

class LogAnalyzer:
	def __init__(self):
		self.D = {}
		self.cnt_qc_match = 0
		self.cnt_c_only = 0
		self.errcnt_q = 0	
		self.errcnt_c = 0	

	def query_log(self, fname):
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
			d = get_qlog_line_dict(flds[1:])
			res =  self.add_query(d)	
			if res < 0: 
				self.errcnt_q += 1
	
	def add_query(self, q_log_dict):
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

		# value = {query string, im, click pos]
		value = [q_log_dict['q'], im, -1]
		self.D[qh] = value
		return 1

	def click_log(self, fname):
		try:
			fp = open(fname)
			print "Open:", fname
		except:
			return

		self._click_lines(fp)

	def _click_lines(self, lineiter):
		for i,line in enumerate(lineiter):
			if (i & 0xFFFF) == 1: time.sleep(0.01)
			flds = line.split('|@')
			# fld0=time, fld1=qh, fld4=click position, fld5=doc ID
			if len(flds) != 9: 
				self.errcnt_c += 1
				continue
			try:
				self.add_click(flds[1], int(flds[4]))
			except:
				self.errcnt_c += 1
				#print flds

	def add_click(self, qh, click_pos):
		try:
			value = self.D[qh]
			value[2] = click_pos
			self.cnt_qc_match += 1
			
		except:
			#print "query Not Found for", qh
			self.cnt_c_only += 1
			

	def print_info(self):
		cnt = 0
		for k,v in self.D.iteritems():
			print k, v
			cnt += 1	
			if cnt > 10: break

	def get_rate(self):
		print "self.errcnt_q", self.errcnt_q
		print "self.errcnt_c", self.errcnt_c
		print "self.cnt_qc_match", self.cnt_qc_match
		print "self.cnt_c_only", self.cnt_c_only

		d = {}
		"""
		d['iqry'] = [0, 0, 0]
		d['ac'] = [0, 0, 0]
		d['pop'] = [0, 0, 0]
		d['tag'] = [0, 0, 0]
		d['more'] = [0, 0, 0]
		d['null'] = [0, 0, 0]
		d[''] = [0, 0, 0]
		"""
		cnt = 0
		for k,v in self.D.iteritems():
			try:
				cnter = d[v[1]] # counter per 'im'
			except:
				cnter = [0, 0, 0]
				d[v[1]] =  cnter

			cnter[0] += 1
			if v[2] != -1: 
				# value = {query string, im, click pos]
				cnter[1] += 1
				cnter[2] += v[2]
				#d[v[1]] = cnter
				cnt += 1

		print "Total=%d, Hit=%d, Ratio=%f" % (len(self.D), cnt, (float(cnt)/len(self.D)*100.0))
		print "'====="
		ranked = sorted(d.iteritems(), key=lambda x:x[1][0], reverse=True)
		for (k,v) in ranked:
			print "im=%s , %s" % (k, ' , '.join( map(str, v)))

		#for k,v in d.iteritems():
		#	print "im=%s , %s" % (k, ' , '.join( map(str, v)))

if __name__=="__main__":
	analyzer = LogAnalyzer()
	#analyzer.query_log('euospcomp07.osp_query.log.20130125')
	#analyzer.query_log('euospcomp08.osp_query.log.20130125')
	#analyzer.query_log('euospsch01.osp_query.log.20130125')
	#analyzer.query_log('euospsch03.osp_query.log.20130125')
	analyzer.query_log('euospsch01.2.osp_query.log.20130125')
	analyzer.query_log('euospsch03.2.osp_query.log.20130125')
	analyzer.click_log('euospsch03.osp_click.log.20130125')
	analyzer.click_log('euospcomp08.osp_click.log.20130125')
	analyzer.print_info()
	analyzer.get_rate()
