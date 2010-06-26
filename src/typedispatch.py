import functools
import inspect

__all__ = ('dispatch', 'inside','empty',)

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
                                   [((), (), old_function)])
        else:
            dispatch_table = []

        dispatch_table.append((dispatch_args, dispatch_kwargs, method))

        @functools.wraps(method)
        def _wrapper(*args, **kwargs):
            return _dispatcher(args, kwargs, dispatch_table)
        _wrapper._f_dispatch_table = dispatch_table

        return _wrapper
    return _decorator


def _check_filter(filter_exp, arg):
    if isinstance(filter_exp, type):
        if not isinstance(arg, filter_exp):
            return False
    elif callable(filter_exp):
        if not filter_exp(arg):
            return False
    else:
        if filter_exp != arg:
            return False
    return True

def _dispatcher(args, kwargs, dispatch_table):
    for dispatch_args, dispatch_kwargs, func in dispatch_table:
        if not dispatch_args and not dispatch_kwargs:
            return func(*args, **kwargs)
        failed = False
        for i, filter_exp in enumerate(dispatch_args):
            arg = args[i]
            if not _check_filter(filter_exp, arg):
                failed = True
                break

        for key, filter_exp in dispatch_kwargs.items():
            if key not in kwargs:
                failed = True
                break
            if not _check_filter(filter_exp, kwargs[key]):
                failed = True
                break
        if failed:
            continue
        return func(*args, **kwargs)
    raise ValueError("Dispatched value not found: %r <=> %r" % (args, dispatch_table))

# helper functions

def inside(*args):
    def _predicate(arg):
        return arg in args
    return _predicate

def empty(arg):
    return not arg
