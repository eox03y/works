import sys
import md5
m = md5.new()
name = sys.argv[1]
name = name[0].upper() + name[1:]

name = name.decode('ascii')
print type(name), name
m.update(name)
hexkey = m.hexdigest()
print hexkey

name = name.encode('ascii')
print type(name), name
m.update(name)
hexkey = m.hexdigest()
print hexkey
