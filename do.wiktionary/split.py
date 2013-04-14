import codecs
import sys

fp = codecs.open(sys.argv[1], 'rb', encoding='utf-8')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

for line in fp:
	line = line.strip()
	for fld in line.split(""","""):
		print fld

