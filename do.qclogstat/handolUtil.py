#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from operator import itemgetter
import codecs
import time
import datetime
import operator

def y_or_n(prompt):
	"""
	y_or_n(prompt)
	    this is just a command-line question
	"""
	s = raw_input(prompt + ' (y/n) ? ')
	if s == "y":
		print "yes"
		return 1
	else:
		print "no"
		return 0

def convert_key_2_str(d):
	newd = {}
	for k,v in d.iteritems():
		newd[str(k)] = v
	return newd
	
def make_dict_w_key(key_list, val_list):
	newd = {}
	for i,k in enumerate(key_list):
		newd[k] = val_list[i]
	return newd

###
def dict_merge_to_new(a, b, func=None):
    # new dict 'r'
    r = dict(a)

    if func==None: func = operator.add
    for k,vb in b.iteritems():
        va = r.get(k, None)
        if va!=None:
            r[k] = func(va, vb)
        else:
            r[k] = vb
    return r

def dict_merge_to_a(a, b, func=None):    
    if func==None: func = operator.add
    for k,vb in b.iteritems():
        va = a.get(k, None)
        if va!=None:
            a[k] = func(va, vb)
        else:
            a[k] = vb
    
def dict_merge_to_a_for_list_value(a, b, func=lambda x,y:map(operator.add, x,y)):    
    if func==None: func = operator.add
    for k,vb in b.iteritems():
        va = a.get(k, None)
        if va!=None:
            a[k] = func(va, vb)
        else:
            a[k] = vb


def dict_merge_to_a_sum(a, b):    
    for k,vb in b.iteritems():
        va = a.get(k, None)
        if va!=None:
            if type(va)==list:
                a[k] = map(operator.add, va, vb)
            else:
                a[k] = va + vb
        else:
            a[k] = vb
			
###	
class TwoCounterDict(dict):        
	def __init__(self):
		super(TwoCounterDict, self).__init__()
		self.ranked = None

	def add_1(self, key):
		cnt = self.setdefault(key, [0,0])
		cnt[0] += 1
		return cnt[0]

	def add_2(self, key):
		cnt = self.setdefault(key, [0,0])
		cnt[1] += 1
		return cnt[1]

	def rank(self):
		# rank high those which has high counter value
		self.ranked = sorted(self.iteritems(), key=lambda x:x[1][0]+x[1][1], reverse=True)

	def sum_of_tops(self, mincnt=0):
		""" get the sum of top 'n' values """
		if self.ranked == None: self.rank()
		i = 0
		s = 0
		for (key, val) in self.ranked:
			s += sum(val)
			i += 1
			if mincnt != 0 and i > mincnt: break
		return s


	def prn(self, mincnt=0):
		if self.ranked == None: self.rank()
		# rank high those which has high counter value
		i = 0
		print "## TOTAL = %d (%d)" % (len(self), mincnt)  
		for (key, val) in self.ranked:
			cnt = sum(val) 
			print "%4d , %4d , %s" % (val[0], val[1], key)
			i += 1
			if mincnt != 0 and i > mincnt: break
	

class CounterDict(dict):        
	def __init__(self):
		super(CounterDict, self).__init__()
		self.ranked = None

	def add(self, key):
		# key, value
		cnt = 1 + self.get(key, 0)
		self[key] = cnt
		return cnt

	def rank(self):
		# rank high those which has high counter value
		self.ranked = sorted(self.iteritems(), key=itemgetter(1), reverse=True)

	def sum_of_tops(self, mincnt=0):
		""" get the sum of top 'n' values """
		if self.ranked == None: self.rank()
		i = 0
		s = 0
		for (key, cnt) in self.ranked:
			s += cnt
			i += 1
			if mincnt != 0 and i > mincnt: break
		return s

	def prn(self, mincnt=0):
		# rank high those which has high counter value
		if self.ranked == None: self.rank()
		i = 0
		print "## TOTAL = %d (%d)" % (len(self), mincnt)  
		for (key, cnt) in self.ranked:
			print "%4d , %s" % (cnt, key)
			i += 1
			if mincnt != 0 and i > mincnt: break

####
#### Values must be 'list' type
class AddValueDict(dict):        
	def __init__(self, myname=''):
		super(AddValueDict, self).__init__()
		self.ranked = None
		self.myname = myname
		self.order = "value"

	def set_order(self, order):
		self.order = order

	def add(self, key, val):
		# key, value
		#if type(val)==list: return None
		prev = self.get(key)
		if prev==None: 
			newval = val
		else:		
			newval = map(operator.add, prev, val)
		self[key] = newval
		return newval

	def rank(self):
		if self.ranked != None: return
		# rank high those which has high counter value
		if self.order=="key":
			self.ranked = sorted(self.iteritems(), key=lambda x:x[0],  reverse=False)
		else:
			self.ranked = sorted(self.iteritems(), key=lambda x:x[1][0],  reverse=True)

	def sum_of_tops(self, mincnt=0):
		""" get the sum of top 'n' values """
		if self.ranked == None: self.rank()
		if len(self.ranked)==0: return []
		if mincnt > len(self.ranked): mincnt = len(self.ranked)
		i = 0
		try:
			sumval = [0] * len(self.ranked[0][1]) # length of value (list)
		except:
			print self.ranked[0]
			raise
		for key, val in self.ranked:
			sumval = map(operator.add, sumval, val)
			i += 1
			if mincnt != 0 and i > mincnt: break
		return sumval

	def prn(self, mincnt=0):
		# rank high those which has high counter value
		if self.ranked == None: self.rank()
		if len(self.ranked)==0: return []
		if mincnt > len(self.ranked): mincnt = len(self.ranked)
		i = 0
		sumval = [0] * len(self.ranked[0][1]) # length of value (list)
		print "## %s TOTAL = %d (%d)" % (self.myname, len(self), mincnt)  
		for key, val in self.ranked:
			valout = " , ".join(map(str, val))
			print "%s , %s" % (key, valout)
			sumval = map(operator.add, sumval, val)
			i += 1
			if mincnt != 0 and i > mincnt: break
		valout = " , ".join(map(str, sumval))
		print "ALLSUM , %s" % (valout)
	
	def save(self, fname, mincnt=0):
		# rank high those which has high counter value
		if self.ranked == None: self.rank()
		if len(self.ranked)==0: return []
		if mincnt > len(self.ranked): mincnt = len(self.ranked)
		
		outf = codecs.open(fname, 'wb', encoding='utf-8')		
		i = 0
		sumval = [0] * len(self.ranked[0][1]) # length of value (list)
		outf.write("%s , TOTAL:%d , PRINT:%d\n" % (self.myname, len(self), mincnt))
		for key, val in self.ranked:
			valout = " , ".join(map(str, val))
			outf.write("%s , %s\n" % (key, valout))
			sumval = map(operator.add, sumval, val)
			i += 1
			if mincnt != 0 and i > mincnt: break
		valout = " , ".join(map(str, sumval))
		outf.write("ALLSUM , %s\n" % (valout))
		outf.close()
		
	def save_key_last(self, fname, mincnt=0):
		# rank high those which has high counter value
		if self.ranked == None: self.rank()
		if len(self.ranked)==0: return []
		
		outf = codecs.open(fname, 'wb', encoding='utf-8')
		
		i = 0
		sumval = [0] * len(self.ranked[0][1]) # length of value (list)
		outf.write("%s\tTOTAL:%d\tPRINT:%d\n" % (self.myname, len(self), mincnt))
		for key, val in self.ranked:
			valout = u"\t".join(map(str, val))
			outf.write("%s\t%s\n" % (valout, key))
			sumval = map(operator.add, sumval, val)
			i += 1
			if mincnt != 0 and i > mincnt: break
		valout = "\t".join(map(str, sumval))
		outf.write("%s\tALLSUM\n" % (valout))
		outf.close()

###
class ListDict(dict):        
	def add(self, key, val):
		# key, value
		try:
			self[key].append(val)
		except:
			self[key] = [val]			

##
class LastKeyDict(dict):        
	def add(self, key, val):
		# key, value
		self[key] = val

##
class FirstKeyDict(dict):        
	def add(self, key, val):
		if not self.has_key(key):
			# key, value
			self[key] = val

			#### Utils
# 1,234 --> 1234
def conv_number2int(num):
	num = filter(str.isdigit, num)
	return int(num)
	
def mk_comma_numstr(numstr):
	n = len(numstr)
	cnt = 3
	resstr = ""
	for i in range(len(numstr)):
		j = len(numstr) - i
		if (j % 3) == 0 and j != len(numstr):
			resstr += ','
		resstr += numstr[i]
	return resstr

#
def datestr_now():
	daystr = time.strftime("%Y-%m-%d-%H", time.localtime(int(time.time())))
	# tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
	return daystr

####
def parse_datetime():
	dateval1 = time.strptime("25-01-2013 00:00:03:238", "%d-%m-%Y %H:%M:%S:%f")
	dateval2 = time.strptime("25-01-2013 00:00:03:938", "%d-%m-%Y %H:%M:%S:%f")
	oneday = datetime.timedelta(days=1)

	
def get_val_in_square(line):
	p1 = line.find('[')
	if p1==-1: 
		return ''
	p2 = p1+1
	while p2 < len(line):
		if line[p2] == ']': 
			return line[p1+1:p2]
		p2 += 1
	return ''		


def get_timestr(line):
	flds = line[:30].split()
	if len(flds) < 2:
		return "2011-00-00 00:00:00"
	if flds[0][0]=="[":
		daystr = flds[0][1:]
	else:
		daystr = "20" + flds[0]

	if flds[1][-1]=="]":
		timestr = flds[1][:8]
	else:
		timestr = flds[1]
	
	return daystr + " " + timestr

###
##
def get_day_list(startday, endday, dformat="%Y%m%d"):
	''' startday, endday is string. 
		ex) 2011-10-07 2011-10-12
	'''
	s = map(int, startday.split('-'))
	e = map(int, endday.split('-'))
	# step = 1 day. use 'date' object
	oneday = datetime.timedelta(days=1)
	start = datetime.date(s[0], s[1], s[2])
	end = datetime.date(e[0], e[1], e[2])
	#today = datetime.date.today()
	res = []
	while start <= end:
		res.append(start.strftime(dformat))
		start += oneday
	return res


### Convert timedelta to Integer or Float number

def timediff2int(t2, t1):
	td = t2 - t1
	return timedelta2int(td)

def timedelta2float(td):
	try:
		res = td.microseconds/float(1000000) + (td.seconds + td.days * 24 * 3600)
		return res
	except:
		return -1

def timedelta2int(td):
	try:
		res = round(td.microseconds/float(1000000)) + (td.seconds + td.days * 24 * 3600)
		return int(res)
	except:
		return -1


###
class StopWatch:	
	def __init__(self):
		self.startval = datetime.datetime.now()
		
	def start(self):
		self.startval = datetime.datetime.now()
		
	def laptime(self):
		nowval = datetime.datetime.now()
		try:
			lapval = timedelta2float(nowval - self.startval)
		except:
			print "Call start() first"
			return 0.0
		self.startval = nowval
		return lapval
	
		
######
if __name__=="__main__":
	if len(sys.argv) < 3:
		print "usage: start_day end_day"
		print "usage: 2011-10-7 2011-10-13"
		sys.exit()
	daylist = get_day_list(sys.argv[1],sys.argv[2])
	for daystr in daylist:
		print daystr

