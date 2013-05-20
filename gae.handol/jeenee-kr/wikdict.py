# -*- coding: utf-8 -*-
import codecs
import sys
import re
import anyReader

from google.appengine.ext import blobstore

''' enwiktionary-20130415.dict.sorted '''
dictfile_key = 'AMIfv97JpUZdTYhEDUrBhVcaO1HjosFX28DXNOfRLdAIQlfYKJAl7IubkTW_w7KD2bUhQZLM79DUF8_hB7IDiphCZk6xLIFYUtda5IEAJJSD1T6JHVbLIAIgtexhMDvJrql2zXywJ6T8tKcmcNU9KnQbHxcrjIx5Lg'
dictfd = None

''' enwiktionary-20130415.index '''
idxfile_key = 'AMIfv95UmXhaoSljjBKr6dv1902AvMwrTQDa3TEbwsG0pmauXuyhIws2GkVDCqgBo6Jb2TcTH1wGt4h0xssmpi4Q5QWdbzhAwYRUeHOfH-8_p7CQZw0JvGEjMlRZ7_0fbZBmAqw5K3nytjt9D8HnopZROUYBeqTKMA'

idxlist = {}

'''
'''
def	read_dict(dictfd, offset, length):
	dictfd.seek(offset)
	content = dictfd.read(length)
	return content

'''
'''
def load_index(idxfd):
	idxlist = {}
	for line in idxfd:
		flds = line.split('\t')
		headword = flds[2].rstrip()
		offset = int(flds[0], 16)
		length = int(flds[1], 16)
		idxlist[headword] = (offset, length)
	idxfd.close()
	return idxlist


'''
'''
def prepare():
	# load index file
	idxfd = blobstore.BlobReader(idxfile_key)
	global idxlist
	idxlist = load_index(idxfd)
	idxfd.close()

	global dictfd
	dictfd = blobstore.BlobReader(dictfile_key)

def lookup_dict(word):
	info = idxlist.get(word, None)
	if not info: 
		return 'NO word'
	else: 
		return read_dict(dictfd, info[0], info[1])

