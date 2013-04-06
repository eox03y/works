## Get Wikitionary Dump Fully
 * wget http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-pages-meta-current.xml.bz2
## Partial Download
 * curl --header "Range: bytes=0-500000" -o enwiktionary.500k.xml.bz2 http://dumps.wikimedia.org/enwiktionary/20130313/enwiktionary-20130313-pages-meta-current.xml.bz2
## Parse & convert wiktionary to simple wiki format
 * python wikxml2dict.py enwiktionary.500k.xml.bz2 > enwiktionary.500k.dict
## Build index file of dict file
