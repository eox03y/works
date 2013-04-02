#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = 0
current_rcount = 0
current_mcount = 0

word = None

for line in sys.stdin:

	
	sp = line.split('\t')
	
	word = sp[0]
	count = sp[1]
	rcount = sp[2]
	mcount = sp[3]
	
	try:
		count = int(count)
		rcount = int(rcount)
		mcount = int(mcount)
	except ValueError:
		continue;
		
	if current_word == word:
		current_count += count
		current_rcount += rcount
		current_mcount += mcount
	else:
		if current_word:
			print '%s\t%s\t%s\t%s' % ( current_word, current_count, current_rcount, current_mcount)
		current_count = count
		current_rcount = rcount
		current_mcount = mcount
		current_word = word

if current_word == word:
	print '%s\t%s\t%s\t%s' % ( current_word, current_count, current_rcount, current_mcount)


