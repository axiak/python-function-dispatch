from typedispatch import *


@dispatch(inside(0, 1))
def fib(n):
    return 1

@dispatch()
def fib(n):
    return fib(n - 1) + fib(n - 2)

for i in range(20):
    print i, fib(i)
