# Howto
## Get Wikitionary Dump Fully
 * wget http://dumps.wikimedia.org/enwiktionary/20130415/enwiktionary-20130415-pages-articles.xml.bz2
## Get xml of one wiki item
 * http://en.wiktionary.org/wiki/Special:Export/take
 * http://en.wiktionary.org/wiki/Special:Export/lion

##
 * python wikxml2wiki.py enwik.100k.line.xml enwik.100k.line.wiki
 * python wikxml2dict.py enwik.100k.line.xml enwik.100k.line.dict
 * python wiki2json.py enwik.100k.line.xml enwik.100k.line.json
## 2013/06/20
 * read xml from URL and parse and then get JSON
 * python wiktion2json.py lion lion.json

## Partial Download
 * curl --header "Range: bytes=0-500000" -o enwiktionary.500k.xml.bz2 http://dumps.wikimedia.org/enwiktionary/20130415/enwiktionary-20130415-pages-articles.xml.bz2

##
 * python gzcat_part.py 100000 enwiktionary-20130415-pages-articles.xml.bz2 enwik.100k.line.xml
## Parse & convert wiktionary to simple wiki format
 * time python wikxml2dict.py  enwiktionary-20130415-pages-articles.xml.bz2 enwiktionary-20130415.dict.bz2
 ** -rw-r--r--  1 daeheehan  staff  387292076 Apr 23 01:44 enwiktionary-20130415-pages-articles.xml.bz2
 ** -rw-r--r--  1 daeheehan  staff   76336706 May 18 00:09 enwiktionary-20130415.dict.bz2
 ** real    20m55.033s
 ** user    19m52.525s
 ** sys     1m2.170s

 * bunzip2 -c enwiktionary-20130415.dict.bz2 |  egrep "^@" | sort > b
 ** bunzip2 -c enwiktionary-20130415.dict.bz2 |  egrep "^@" > a
 ** sort a > b
 ** -rw-r--r--  1 daeheehan  staff  50977146 May 18 00:17 b
 ** wc -l b --> 3534117

 * process XML file
 ** python wikxml2dict.py enwiktionary.500k.xml.bz2 enwiktionary.500k.dict.bz2
 ** python wikxml2dict.py enwiktionary.500k.xml.bz2 enwiktionary.500k.dict.gz
 ** python wikxml2dict.py enwiktionary.500k.xml.bz2 enwiktionary.500k.dict
 * 5/13 : process wiki text file
 ** python wikxml2dict.py abdication.wiki  > abdication.dict
## Build index file of dict file
 * python makeidxofdict.py enwiktionary-20130415.dict.bz2 enwiktionary-20130415.index.bz2
 * python makeidxandsort.py enwiktionary-20130415.dict.bz2 enwiktionary-20130415.dict.sorted.bz2 enwiktionary-20130415.index.bz2
 ** real	0m26.233s
 ** user	0m25.949s
 ** sys	0m0.275s

## image url
* https://en.wikipedia.org/w/api.php
* http://www.mediawiki.org/wiki/API:Properties
* http://commons.wikimedia.org/wiki/FAQ#What_are_the_strangely_named_components_in_file_paths.3F
* http://www.md5.cz/ 
* http://en.wiktionary.org/wiki/File:Lion_waiting_in_Namibia.jpg
* http://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Lion_waiting_in_Namibia.jpg/800px-Lion_waiting_in_Namibia.jpg

## wikipedia API: image info
* http://en.wikipedia.org/w/api.php?action=query&titles=Image:Albert%20Einstein%20Head.jpg&prop=imageinfo
* http://en.wikipedia.org/w/api.php?action=query&titles=Image:Albert%20Einstein%20Head.jpg&prop=imageinfo&iiprop=size|url|sha1
* http://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=images
* 
## audio url
* {{audio|En-uk-eschatology.ogg|Audio (UK)}}
* <source src="//upload.wikimedia.org/wikipedia/commons/3/3e/En-uk-eschatology.ogg" type="audio/ogg; codecs=&quot;vorbis&quot;" data-title="Original Ogg file (411 kbps)" data-shorttitle="Ogg source" data-width="0" data-height="0" data-bandwidth="411402"></source>
* http://en.wiktionary.org/wiki/File:En-uk-eschatology.ogg
* http://upload.wikimedia.org/wikipedia/commons/3/3e/En-uk-eschatology.ogg


## read one XML directly from wiktionary site
* python wikxml2wiki.py http://en.wiktionary.org/wiki/Special:Export/lion a
* python wikxml2dict.py http://en.wiktionary.org/wiki/Special:Export/lion b

python2.6 wikxml2imglist.py /home/ktmtdata/wikipedia/enwiktionary-20130814-pages-articles.xml.bz2 /home/ktmtdata/wikipedia/wiktion_img.txt &

