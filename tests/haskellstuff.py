from typedispatch import *

# implementation of
# reverse' :: [a] -> [a]  
# reverse' [] = []  
# reverse' (x:xs) = reverse' xs ++ [x]  

@dispatch(empty)
def reverse(l):
    return []

@dispatch()
def reverse(l):
    x, xs = l[0], l[1:]
    return reverse(xs) + [x]



print reverse([1, 2, 3])
