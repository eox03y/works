import sys
import os
import platform
import site

if 'Windows' in platform.platform():
    SUFFIXES = [
        '',
        'lib/site-packages',
        ]
else:
    SUFFIXES = [
        'lib/python%s/site-packages' % sys.version[:3],
        'lib/site-python',
        ]

print 'Path prefixes:'
for p in site.PREFIXES:
    print '  ', p

for prefix in sorted(set(site.PREFIXES)):
    print
    for suffix in SUFFIXES:
        path = os.path.join(prefix, suffix).rstrip(os.sep)
        print path
        print '   exists:', os.path.exists(path)
        print '  in path:', path in sys.path


print 'Base:', site.USER_BASE
print 'Site:', site.USER_SITE

