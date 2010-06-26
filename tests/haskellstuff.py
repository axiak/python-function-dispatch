from typedispatch import *

import timeit

# implementation of
# reverse' :: [a] -> [a]  
# reverse' [] = []  
# reverse' (x:xs) = reverse' xs ++ [x]  

@dispatch(())
def reverse(l):
    return []

@dispatch(iterable)
def reverse(l):
    return reverse(l[1:]) + l[:1]


print reverse([1, 2, 3])

def normal_reverse(l):
    if not l:
        return []
    return normal_reverse(l[1:]) + l[:1]

print "Generic dispatch:"
print timeit.timeit(lambda : reverse([1, 2, 3, 4, 5, 6, 7]), number=10000)

print "Standard recursive:"
print timeit.timeit(lambda : normal_reverse([1, 2, 3, 4, 5, 6, 7]), number=10000)
