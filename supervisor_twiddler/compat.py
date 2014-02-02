import sys

PY3 = sys.version_info[0] == 3

if PY3:
    basestring = str
    class unicode(str):
        def __init__(self, string, encoding, errors):
            str.__init__(self, string)
else:
    basestring = basestring
    unicode = unicode
