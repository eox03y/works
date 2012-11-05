import re

def trim_whitespace(orgstr):
	pattern = re.compile("(\r\n)", re.I)

