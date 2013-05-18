time wget http://dumps.wikimedia.org/enwiktionary/20130415/enwiktionary-20130415-pages-articles.xml.bz2

time python wikxml2dict.py  enwiktionary-20130415-pages-articles.xml.bz2 enwiktionary-20130415.dict.bz2

time python makeidxandsort.py enwiktionary-20130415.dict.bz2 enwiktionary-20130415.dict.sorted.bz2 enwiktionary-20130415.index.bz2

