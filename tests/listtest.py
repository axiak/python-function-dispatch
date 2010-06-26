from typedispatch import *


@dispatch(['1', int, iterable])
def tester(l):
    one, n, blah = l
    print "%s, %s" % (one, n + 1)


tester(['1', 5, [10]])
