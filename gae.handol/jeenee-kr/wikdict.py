# -*- coding: utf-8 -*-
import codecs
import sys
import re
import anyReader
import md5

from google.appengine.ext import blobstore

''' enwiktionary-20130415.dict.sorted '''
dictfile_key = 'AMIfv97JpUZdTYhEDUrBhVcaO1HjosFX28DXNOfRLdAIQlfYKJAl7IubkTW_w7KD2bUhQZLM79DUF8_hB7IDiphCZk6xLIFYUtda5IEAJJSD1T6JHVbLIAIgtexhMDvJrql2zXywJ6T8tKcmcNU9KnQbHxcrjIx5Lg'
dictfd = None

''' enwiktionary-20130415.index '''
idxfile_key = 'AMIfv95UmXhaoSljjBKr6dv1902AvMwrTQDa3TEbwsG0pmauXuyhIws2GkVDCqgBo6Jb2TcTH1wGt4h0xssmpi4Q5QWdbzhAwYRUeHOfH-8_p7CQZw0JvGEjMlRZ7_0fbZBmAqw5K3nytjt9D8HnopZROUYBeqTKMA'

idxlist = {}

def get_sound_div(oggfile):
	m = md5.new()
	m.update(oggfile)
	hexkey = m.hexdigest()
	folder = '%s/%s' % (hexkey[0], hexkey[:2])
	snddiv = ''' <div class="mediaContainer" style="position:relative;display:block;width:175px">
	<audio id="mwe_player_0" style="width:175px;height:23px" poster="//bits.wikimedia.org/static-1.22wmf4/skins/common/images/icons/fileicon-ogg.png" controls="" preload="none" class="kskin" data-durationhint="1.3815873015873" data-startoffset="0" data-mwtitle="%s" data-mwprovider="wikimediacommons">
	<source src="//upload.wikimedia.org/wikipedia/commons/%s/%s" type="audio/ogg; codecs=&quot;vorbis&quot;" data-title="Original Ogg file (107 kbps)" data-shorttitle="Ogg source" data-width="0" data-height="0" data-bandwidth="107280"></source>
	''' % (oggfile, folder, oggfile)
	return snddiv

'''
[[Image:Lion waiting in Nambia.jpg|thumb|right|250px|A lion.]]
'''
def get_image_div(imgdesc):
	imgdesc = imgdesc[8:-2]
	flds = imgdesc.split('|')
	if len(flds) < 5: 
		return '<div class="dictimg"></div>'

	imgfile = flds[0]
	desc = flds[4]	
	m = md5.new()
	m.update(imgfile)
	hexkey = m.hexdigest()
	folder = '%s/%s' % (hexkey[0], hexkey[:2])
	imgurl = 'http://upload.wikimedia.org/wikipedia/commons/%s/%s' % (folder, imgfile)

	imgdiv = '''<div class="dictimg"> <img src="%s"> %s </img></div>''' % (imgurl, desc)
	return imgdiv

def	read_dict(dictfd, offset, length):
	dictfd.seek(offset)
	content = dictfd.read(length)
	return content

def dict2html(content):
	html = ''
	for line in content.splitlines():
		if line[0]=='@':
			hline = '<div class="hword"> %s </div>' % (line[2:])
			html += hline
		elif line[0]=='#:':
			hline = '<div class="exstc"> %s </div>' % (line[2:])
			html += line
		elif line[0]=='#':
			hline = '<div class="meaning"> %s </div>' % (line[2:])
			html += line

		elif line.endswith('.ogg'):
			html += get_sound_div(line)

		elif line.startswith('[[Image'):
			html += get_image_div(line)

		else:
			pass
	return html
			
	
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
		dicttxt = read_dict(dictfd, info[0], info[1])
		html = dict2html(dicttxt)
		return html

