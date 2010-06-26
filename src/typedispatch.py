import functools
import inspect
import re

from itertools import izip_longest

__all__ = ('dispatch', 'inside', 'anything', 'iterable', 'regexsingle', 'regexmulti')

NoRewrite = object()

def dispatch(*dispatch_args, **dispatch_kwargs):
    def _decorator(method):
        func_name = method.__name__
        try:
            stack_frame = inspect.stack()[1][0]
        except IndexError:
            raise Exception("Could not interpret the stack!")

        old_function = stack_frame.f_locals.get(func_name, None)
        if old_function:
            dispatch_table = getattr(old_function, '_f_dispatch_table',
                                     [])
        else:
            dispatch_table = []

        idx = -1
        # Logic for inserting before generic default.
        for idx in range(len(dispatch_table) - 1, -1, -1):
            if dispatch_table[idx][0] or dispatch_table[idx][1]:
                break

        dispatch_table.insert(idx + 1, (dispatch_args, dispatch_kwargs, method))

        @functools.wraps(method)
        def _wrapper(*args, **kwargs):
            return _dispatcher(args, kwargs, dispatch_table)
        _wrapper._f_dispatch_table = dispatch_table

        return _wrapper
    return _decorator


def _check_filter(filter_exp, arg):
    #print 'Check: %r <=> %r' % (filter_exp, arg)
    if isinstance(filter_exp, type):
        if not isinstance(arg, filter_exp):
            return False, NoRewrite

    elif callable(filter_exp):
        result = filter_exp(arg)
        if isinstance(result, (list, tuple)):
            return result[0], result[1]
        return bool(result), NoRewrite

    elif hasattr(filter_exp, '__iter__'):
        if not hasattr(arg, '__iter__'):
            return False, NoRewrite
        BAD = object()
        rewritten_arglist = []
        for sub_filter_exp, sub_arg in izip_longest(filter_exp, arg, fillvalue=BAD):
            if sub_filter_exp is BAD or sub_arg is BAD:
                return False, NoRewrite
            result, rewrite = _check_filter(sub_filter_exp, sub_arg)
            if not result:
                return False, NoRewrite
            
            # Rewrite inside a list
            if rewrite is not NoRewrite:
                rewritten_arglist.append(rewrite)
            else:
                rewritten_arglist.append(sub_arg)
        return True, rewritten_arglist
    else:
        return filter_exp == arg, NoRewrite
    return True, NoRewrite


def _dispatcher(args, kwargs, dispatch_table):
    for dispatch_args, dispatch_kwargs, func in dispatch_table:
        if not dispatch_args and not dispatch_kwargs:
            return func(*args, **kwargs)
        failed = False
        new_args = list(args)
        for i, filter_exp in enumerate(dispatch_args):
            arg = args[i]
            result, rewrite = _check_filter(filter_exp, arg)
            if not result:
                failed = True
                break
            if rewrite is not NoRewrite:
                new_args[i] = rewrite

        new_kwargs = dict(kwargs)

        for key, filter_exp in dispatch_kwargs.items():
            if key not in kwargs:
                failed = True
                break
            result, rewrite = _check_filter(filter_exp, kwargs[key])
            if not result:
                failed = True
                break
            if rewrite is not NoRewrite:
                new_kwargs[key] = rewrite
        if failed:
            continue
        return func(*new_args, **new_kwargs)
    raise NameError("named function %r with arguments is not defined" % func.__name__)

# helper functions

def inside(*args):
    def _predicate(arg):
        return arg in args
    return _predicate

def anything(*args):
    return True

def iterable(arg):
    return hasattr(arg, '__iter__')


def regexmulti(regex, flags=0):
    compiled = re.compile(regex, flags)
    def _result(text):
        matches = list(compiled.finditer(text))
        if matches:
            return True, matches
        else:
            return False
    return _result

def regexsingle(regex, flags=0):
    compiled = re.compile(regex, flags)
    def _result(text):
        match = compiled.search(text)
        if match:
            return True, match
        else:
            return False
    return _result
