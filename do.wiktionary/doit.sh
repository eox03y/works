# http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-pages-meta-current.xml.bz2
#
python gzcat_part.py 5000 /home/search/disk2/wiki_visit_count/wiktionary/enwiktionary-20130313-abstract.xml.gz enwiktionary-20130313-abstract.xml.5000



python wiktio2xml.py enwiktionary-20130313-pages-meta-current.20k.xml a -q > b
python wikxml2dict.py enwiktionary-20130313-pages-meta-current.20k.xml > i
python wikxml2dict.py http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-image.sql.gz > a
python wikxml2dict.py http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-imagelinks.sql.gz > b
python wikxml2dict.py http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-pages-meta-current.xml.bz2 > c
python wikxml2dict.py http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-pages-articles-multistream-index.txt.bz2 > d


# full
python wikxml2dict.py /home/search/disk2/wiki_visit_count/wiktionary/enwiktionary-20130313-pages-meta-current.xml.bz2 | bzip2 -c > /home/search/disk2/wiki_visit_count/wiktionary/good.bz2

# partial
python gzcat_part.py 100000 /home/search/disk2/wiki_visit_count/wiktionary/enwiktionary-20130313-pages-meta-current.xml.bz2 enwiktionary.100k.xml
python wikxml2dict.py enwiktionary.100k.xml > enwiktionary.dict


# image url
# ex) Image:Albert Einstein Head.jpg
wget http://en.wikipedia.org/w/api.php\?action=query\&titles=Image:Albert%20Einstein%20Head.jpg\&prop=imageinfo\&iiprop=url\&iiurlwidth=200
curl http://en.wikipedia.org/w/api.php\?action=query\&titles=Image:Albert%20Einstein%20Head.jpg\&prop=imageinfo\&iiprop=url\&iiurlwidth=200\&format=json -o imgThumb.2.txt
curl http://en.wikipedia.org/w/api.php\?action=query\&titles=File:Albert%20Einstein%20Head.jpg\&prop=imageinfo\&iiprop=url\&iiurlwidth=200\&format=json -o imgThumb.3.txt

