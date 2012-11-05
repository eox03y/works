import difflib

A = """aa
hhh
bb
cc
dd"""

B = """aa
bb
bbb
cc
cccc
d
dd
ddd"""

A = A.splitlines()
B = B.splitlines()

print A
print B

d = difflib.ndiff(A,B)
for a in d:
	print a

d = difflib.context_diff(A,B)
for a in d:
	print a

