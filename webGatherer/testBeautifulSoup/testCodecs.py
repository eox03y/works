latin1word = 'Sacr\xe9 bleu!'
unicodeword = unicode(latin1word, 'latin-1')
try:
	print unicodeword
except:
	print unicodeword.encode('euc-kr', 'ignore')

