time curl -O http://dumps.wikimedia.org/enwiktionary/20130415/enwiktionary-20130415-pages-articles.xml.bz2

time python wikxml2dict.py  enwiktionary-20130415-pages-articles.xml.bz2 enwiktionary-20130415.dict.bz2

time python makeidxandsort.py enwiktionary-20130415.dict.bz2 enwiktionary-20130415.dict.sorted.bz2 enwiktionary-20130415.index.bz2


### result : iMac
-rw-r--r--  1 jiinhan  staff  387292076  4 16 03:31 enwiktionary-20130415-pages-articles.xml.bz2
-rw-r--r--  1 jiinhan  staff   38132712  5 21 01:32 enwiktionary-20130415.dict.bz2
-rw-r--r--  1 jiinhan  staff   37287180  5 21 01:32 enwiktionary-20130415.dict.sorted.bz2
-rw-r--r--  1 jiinhan  staff    4283833  5 21 01:32 enwiktionary-20130415.index.bz2



