import sys

PY3 = sys.version_info[0] == 3

if PY3:
    basestring = str
    class unicode(str):
        def __init__(self, string, encoding, errors):
            str.__init__(self, string)

    def _b(x, encoding='latin1'):
        # x should be a str literal
        return bytes(x, encoding)

    def _u(x, encoding='latin1'):
        # x should be a str literal
        if isinstance(x, str):
            return x
        return str(x, encoding)
else:
    basestring = basestring
    unicode = unicode

    def _b(x, encoding='latin1'):
        # x should be a str literal
        return x

    def _u(x, encoding='latin1'):
        # x should be a str literal
        return unicode(x, encoding)
