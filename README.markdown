# Generic Dispatch for Python

This is a very basic generic dispatch system for Python.
This is inspired by Haskell's syntax for writing conditional function
definitions, hence the package name.

## Quick intro

You can see examples in the `tests` directory, but here is a very simple
example.

In Haskell you might implement a `reverse` function the following way:

    reverse' :: [a] -> [a]  
    reverse' [] = []  
    reverse' (x:xs) = reverse' xs ++ [x] 

This method uses the type system to define the function for the empty
list and for basically the other case.

Here's the cooresponding solution using this dispatch system:

    from typedispatch import *

    @dispatch([])
    def reverse(l):
        return []

    @dispatch(iterable)
    def reverse(l):
        x, xs = l[0], l[1:]
        return reverse(l[1:]) + l[:1]

So yeah, this is pretty cool syntactic sugar. What happens if we
run `reverse(5)`, which is clearly not defined given the above definition?

    >>> reverse(5)
    Traceback (most recent call last):
        ...
        NameError: named function 'reverse' with arguments is not defined

So we get what we'd expect: the function is not "defined" for this specific
argument.
