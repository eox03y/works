python gzcat_part.py 5000 /home/search/disk2/wiki_visit_count/wiktionary/enwiktionary-20130313-abstract.xml.gz enwiktionary-20130313-abstract.xml.5000

python gzcat_part.py 5000 /home/search/disk2/wiki_visit_count/wiktionary/enwiktionary-20130313-pages-meta-current.xml.bz2 enwiktionary-20130313-pages-meta-current.5000.xml


python wiktio2xml.py enwiktionary-20130313-pages-meta-current.5000.xml a -q > b
