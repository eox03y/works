# Howto
## Get Wikitionary Dump Fully
 * wget http://dumps.wikimedia.org/enwiktionary/20130415/enwiktionary-20130415-pages-articles.xml.bz2

## Partial Download
 * curl --header "Range: bytes=0-500000" -o enwiktionary.500k.xml.bz2 http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-pages-articles.xml.bz2

## Parse & convert wiktionary to simple wiki format
 * time python wikxml2dict.py  enwiktionary-20130415-pages-articles.xml.bz2 enwiktionary-20130415.dict.bz2
 * process XML file
 ** python wikxml2dict.py enwiktionary.500k.xml.bz2 enwiktionary.500k.dict.bz2
 ** python wikxml2dict.py enwiktionary.500k.xml.bz2 enwiktionary.500k.dict.gz
 ** python wikxml2dict.py enwiktionary.500k.xml.bz2 enwiktionary.500k.dict
 * 5/13 : process wiki text file
 ** python wikxml2dict.py abdication.wiki  > abdication.dict
## Build index file of dict file


## image url
* https://en.wikipedia.org/w/api.php
* http://www.mediawiki.org/wiki/API:Properties
* http://commons.wikimedia.org/wiki/FAQ#What_are_the_strangely_named_components_in_file_paths.3F
* http://www.md5.cz/ 
* http://en.wiktionary.org/wiki/File:Lion_waiting_in_Namibia.jpg
* http://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Lion_waiting_in_Namibia.jpg/800px-Lion_waiting_in_Namibia.jpg


## audio url
* {{audio|En-uk-eschatology.ogg|Audio (UK)}}
* <source src="//upload.wikimedia.org/wikipedia/commons/3/3e/En-uk-eschatology.ogg" type="audio/ogg; codecs=&quot;vorbis&quot;" data-title="Original Ogg file (411 kbps)" data-shorttitle="Ogg source" data-width="0" data-height="0" data-bandwidth="411402"></source>
* http://en.wiktionary.org/wiki/File:En-uk-eschatology.ogg
* http://upload.wikimedia.org/wikipedia/commons/3/3e/En-uk-eschatology.ogg


