# -*- coding: utf-8 -*-
import codecs
import sys
import re
import anyReader
import md5
import logging

from google.appengine.ext import blobstore

''' enwiktionary-20130415.dict.sorted '''
dictfile_key = 'AMIfv97JpUZdTYhEDUrBhVcaO1HjosFX28DXNOfRLdAIQlfYKJAl7IubkTW_w7KD2bUhQZLM79DUF8_hB7IDiphCZk6xLIFYUtda5IEAJJSD1T6JHVbLIAIgtexhMDvJrql2zXywJ6T8tKcmcNU9KnQbHxcrjIx5Lg'
dictfd = None

''' enwiktionary-20130415.index '''
idxfile_key = 'AMIfv95UmXhaoSljjBKr6dv1902AvMwrTQDa3TEbwsG0pmauXuyhIws2GkVDCqgBo6Jb2TcTH1wGt4h0xssmpi4Q5QWdbzhAwYRUeHOfH-8_p7CQZw0JvGEjMlRZ7_0fbZBmAqw5K3nytjt9D8HnopZROUYBeqTKMA'

idxlist = {}

def get_sound_div(oggfile):
	m = md5.new()
	oggfile = oggfile[0].upper() + oggfile[1:]
	m.update(oggfile)
	hexkey = m.hexdigest()
	folder = u'%s/%s' % (hexkey[0], hexkey[:2])
	snddiv = u''' <div class="mediaContainer" style="position:relative;display:block;width:175px">
	<audio id="mwe_player_0" style="width:175px;height:23px" poster="//bits.wikimedia.org/static-1.22wmf4/skins/common/images/icons/fileicon-ogg.png" controls="" preload="none" class="kskin" data-durationhint="1.3815873015873" data-startoffset="0" data-mwtitle="%s" data-mwprovider="wikimediacommons">
	<source src="http://upload.wikimedia.org/wikipedia/commons/%s/%s" type="audio/ogg; codecs=&quot;vorbis&quot;" data-title="Original Ogg file (107 kbps)" data-shorttitle="Ogg source" data-width="0" data-height="0" data-bandwidth="107280">
	</source></audio></div> ''' % (oggfile, folder, oggfile)
	return snddiv

'''
[[Image:Lion waiting in Nambia.jpg|thumb|right|250px|A lion.]]
'''
def get_image_div(imgdesc):
	imgdesc = imgdesc[8:-2]
	flds = imgdesc.split('|')
	if len(flds) < 5: 
		return '<div class="dictimg"></div>\n'

	imgfile = flds[0].replace(' ', '_')
	imgfile = imgfile[0].upper() + imgfile[1:]
	desc = flds[4]	
	m = md5.new()
	m.update(imgfile)
	hexkey = m.hexdigest()
	folder = u'%s/%s' % (hexkey[0], hexkey[:2])
	imgurl = u'http://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/800px-%s' % (folder, imgfile, imgfile)

	imgdiv = u'''<div class="dictimg"> <img src="%s"> %s </img></div>\n''' % (imgurl, desc)
	return imgdiv

'''
'''
srch trans_pos = re.compile(r'{{[^}]+}}')
def get_translation_div(trnsline):
	line = trnsline[2:]
	pos = line.find(':')
	if pos == -1: return ''
	lang = line[:pos]
	m = trans_pos.search(line)
	if not m: return ''
				

def	read_dict(dictfd, offset, length):
	dictfd.seek(offset)
	content = dictfd.read(length)
	content = content.decode('utf-8')
	logging.info("dict:")
	logging.info(content)
	return content

def dict2html(content):
	html = u''
	for line in content.splitlines():
		line = line.strip()
		if line[0]=='@':
			hline = u'<div class="hword"> %s </div>\n' % (line[2:])
			html += hline
		elif line[:2]=='#:':
			hline = u'<div class="exstc"> %s </div>\n' % (line[2:])
			html += hline
		elif line[0]=='#':
			hline = u'<div class="meaning"> %s </div>\n' % (line[2:])
			html += hline

		elif line.endswith('.ogg'):
			html += get_sound_div(line)

		elif line.startswith('[[Image'):
			html += get_image_div(line)

		elif line.startswith(''):
			html += get_translation_div(line)

		else:
			pass
	logging.info("html:")
	logging.info(html)
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
	logging.info("prepare() idxlist: size = %d" % (len(idxlist)))

	global dictfd
	dictfd = blobstore.BlobReader(dictfile_key)

def lookup_dict(word):
	info = idxlist.get(word, None)
	logging.info("lookup() idxlist: size = %d, word=%s" % (len(idxlist), word))
	if not info: 
		return 'NO word'
	else: 
		dicttxt = read_dict(dictfd, info[0], info[1])
		html = dict2html(dicttxt)
		return html

