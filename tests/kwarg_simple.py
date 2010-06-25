from typedispatch import *

@dispatch(var=int)
def foo(var):
    return var + 10

@dispatch(var=str)
def foo(var):
    return var.upper()


print foo(var=20)

print foo(var='mike')
