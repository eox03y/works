# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      daehee00.han
#
# Created:     19-02-2013
# Copyright:   (c) daehee00.han 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import sys
import codecs
import operator
from operator import itemgetter

def to_outfile(keyword_list, outf):
    outp = codecs.open(outf, 'wb', encoding='utf-8')
    for v in keyword_list:
        outp.write('%d\t%d\t%d\t%s\n'% (v[1], v[2], v[3], v[0]))
    outp.close()



def from_mongo_jsonfile(fname):
    jlist = []
    if fname=='-':
        #fp = open(sys.stdin.fileno(), 'rb', encoding='utf-8') 
        #fp = codecs.getreader(encoding='utf-8')(sys.in)
        fp = codecs.getreader('utf-8')(sys.stdin)
    else:
        fp = codecs.open(fname, 'rb', encoding='utf-8')
    for line in fp:
        jdata = json.loads(line)
        q = 0
        c = 0
        nores = 0
        for k,v in jdata.iteritems():
            if k.startswith('20'):
		try:
                    q += v['q']
                    c += v['c']
                    nores += v['nores']
                except:
                    pass
	if q > 0:
		jlist.append([jdata['_id'], q, c, nores])
    fp.close()
    #jlist.sort(cmp=lambda x,y: x[1]-y[1])
    jlist.sort(key=itemgetter(1), reverse=True)
    return jlist

def test():
    klist = from_mongo_jsonfile('../keywords.json.head')
    to_outfile(klist, 'keyword.stat')
    pass

if __name__ == '__main__':
    #test()
    klist = from_mongo_jsonfile(sys.argv[1])
    to_outfile(klist, sys.argv[2])
