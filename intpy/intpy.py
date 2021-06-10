import inspect
from functools import wraps
import time

from .function_graph import *
from .data_access import get_cache_data, create_entry, saveNewDataDB, DICT_NEW_DATA
from .logger.log import debug

import multiprocessing
from . import CONN_DB
from .db import DB
import os

def _get_cache(func, args):
    fun_source = get_source_code_executed(func, USER_SCRIPT_GRAPH)
    return get_cache_data(args, fun_source)


def _cache_exists(cache):
    return cache is not None


def _cache_data(func, fun_args, fun_return, elapsed_time):
    debug("starting caching data for {0}({1})".format(func.__name__, fun_args))
    start = time.perf_counter()
    fun_source = get_source_code_executed(func, USER_SCRIPT_GRAPH)
    create_entry(fun_args, fun_return, fun_source)
    end = time.perf_counter()
    debug("caching {0} took {1}".format(func.__name__, end - start))

def _execute_func(f, method_args, method_kwargs, self=None,):    
    start = time.perf_counter()
    result_value = f(self, *method_args, **method_kwargs) if self is not None else f(*method_args, **method_kwargs)
    end = time.perf_counter()

    elapsed_time = end - start

    debug("{0} took {1} to run".format(f.__name__, elapsed_time))

    return (result_value, elapsed_time)


def _method_call(f):
    @wraps(f)
    def wrapper(self, *method_args, **method_kwargs):
        debug("calling {0}".format(f.__name__))
        c = _get_cache(f, method_args)
        if not _cache_exists(c):
            debug("cache miss for {0}({1})".format(f.__name__, *method_args))
            return_value, elapsed_time = _execute_func(f, method_args, method_kwargs, self)
            _cache_data(f, method_args, return_value, elapsed_time)
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
            return_value, elapsed_time = _execute_func(f, method_args, method_kwargs)
            _cache_data(f, method_args, return_value, elapsed_time)
            return return_value
        else:
            debug("cache hit for {0}({1})".format(f.__name__, *method_args))
            return c

    return wrapper


# obs
def _is_method(f):
    args = inspect.getfullargspec(f).args
    return bool(args and args[0] == 'self')


def deterministic(f):
    return _method_call(f) if _is_method(f) else _function_call(f)


def initialize_cache(user_script_path):
    global USER_SCRIPT_GRAPH
    USER_SCRIPT_GRAPH = create_experiment_function_graph(user_script_path)


def save_cache():
    saveNewDataDB()


def initialize_intpy(user_script_path):
    def decorator(f):
        def execution(*method_args, **method_kwargs):
            initialize_cache(user_script_path)
            f(*method_args, **method_kwargs)
            save_cache()
        return execution
    return decorator


USER_SCRIPT_GRAPH = None