import inspect
from functools import wraps
import time

from .data_access import get_cache_data, create_entry
from .logger.log import debug


def _get_cache(func, args):
    return get_cache_data(func.__name__, args, inspect.getsource(func))


def _cache_exists(cache):
    return cache is not None


def _cache_data(func, fun_args, fun_return, elapsed_time):
    debug("starting caching data for {0}({1})".format(func.__name__, fun_args))
    start = time.clock()
    create_entry(func.__name__, fun_args, fun_return, inspect.getsource(func))
    end = time.clock()
    debug("caching {0} took {1}".format(func.__name__, end - start))


def _execute_func(f, self, *method_args, **method_kwargs):
    start = time.clock()
    result_value = f(self, *method_args, **method_kwargs) if self is not None else f(*method_args, **method_kwargs)
    end = time.clock()

    elapsed_time = end - start

    debug("{0} took {1} to run".format(f.__name__, elapsed_time))

    return result_value, elapsed_time


def _method_call(f):
    @wraps(f)
    def wrapper(self, *method_args, **method_kwargs):
        debug("calling {0}".format(f.__name__))
        c = _get_cache(f, method_args)
        if not _cache_exists(c):
            debug("cache miss for {0}({1})".format(f.__name__, *method_args))
            return_value, elapsed_time = _execute_func(f, self, *method_args, **method_kwargs)
            _cache_data(f, method_args, return_value, inspect.getsource(f))
            return return_value
        else:
            debug("cache hit for {0}({1})".format(f.__name__, *method_args))
            return c

    return wrapper


def _function_call(f):
    @wraps(f)
    def wrapper(*method_args, **method_kwargs):
        debug("calling {0}".format(f.__name__))
        c = _get_cache(f, method_args)
        if not _cache_exists(c):
            debug("cache miss for {0}({1})".format(f.__name__, *method_args))
            return_value, elapsed_time = _execute_func(f, *method_args, **method_kwargs)
            _cache_data(f, method_args, return_value, inspect.getsource(f))
            return return_value
        else:
            debug("cache hit for {0}({1})".format(f.__name__, *method_args))
            return c

    return wrapper


# Gambiarra, talvez mude
def _is_method(f):
    args = inspect.getfullargspec(f).args
    return bool(args and args[0] == 'self')


def deterministic(f):
    return _method_call(f) if _is_method(f) else _function_call(f)
