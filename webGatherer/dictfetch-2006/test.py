a = 'aaa'
b = 'bbb'
c = 'ccc'

ll = [c,b,a]

D = {}

print ll[0] is c
print ll
#print "hval=", hash(ll)
kk = (1,2)
D[kk] = 'hhh'

ll.sort()
print ll[0] is c
print ll[0] is a
print ll
#print "hval=", hash(ll)
gg = ('aaaa',2)
D[gg] = 'kkk'

print D.items()

A = {}
for l in ll:
	A[l] = l + ' 123'
	

print A.items()
print A.keys()[0] is a
