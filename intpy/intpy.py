import inspect
import time

from functools import wraps

from intpy.parser_params import get_params
from intpy.environment import init_env
from intpy.logger.log import debug

argsp_v, argsp_no_cache = get_params()

print(argsp_v)

print(argsp_no_cache)

if not argsp_no_cache:
    init_env()
    from intpy.data_access import get_cache_data, create_entry, salvarNovosDadosBanco


"""
v_data_access_import = importlib.import_module(v_data_access, package="intpy")
print(v_data_access_import)

f_get_cache_data = getattr(v_data_access_import, "get_cache_data")
print(f_get_cache_data)

f_create_entry = getattr(v_data_access_import, "create_entry")
print(f_create_entry)

f_salvarNovosDadosBanco = getattr(v_data_access_import, "salvarNovosDadosBanco")
print(f_salvarNovosDadosBanco)
"""


#On the decorator "initialize_intpy", "user_script_path" is declared
#to maintain compatibility between different versions of IntPy
def initialize_intpy(user_script_path):
    def decorator(f):
        def execution(*method_args, **method_kwargs):
            #if not argsp_no_cache:
                #init_env()
            f(*method_args, **method_kwargs)
            if not argsp_no_cache:
                _salvarCache()
        return execution
    return decorator


if argsp_no_cache:
    def deterministic(f):
        return f
else:
    def deterministic(f):
        return _method_call(f) if _is_method(f) else _function_call(f)


def _get_cache(func, args, argsp_v):
    return get_cache_data(func.__name__, args, inspect.getsource(func), argsp_v)


def _cache_exists(cache):
    return cache is not None


def _cache_data(func, fun_args, fun_return, elapsed_time):
    debug("starting caching data for {0}({1})".format(func.__name__, fun_args))
    start = time.perf_counter()
    create_entry(func.__name__, fun_args, fun_return, inspect.getsource(func))
    end = time.perf_counter()
    debug("caching {0} took {1}".format(func.__name__, end - start))


def _execute_func(f, self, *method_args, **method_kwargs):
    start = time.perf_counter()
    result_value = f(self, *method_args, **method_kwargs) if self is not None else f(*method_args, **method_kwargs)
    end = time.perf_counter()

    elapsed_time = end - start

    debug("{0} took {1} to run".format(f.__name__, elapsed_time))

    return result_value, elapsed_time


def _method_call(f):
    @wraps(f)
    def wrapper(self, *method_args, **method_kwargs):
        debug("calling {0}".format(f.__name__))
        c = _get_cache(f, method_args, argsp_v)
        if not _cache_exists(c):
            debug("cache miss for {0}({1})".format(f.__name__, *method_args))
            return_value, elapsed_time = _execute_func(f, self, *method_args, **method_kwargs)
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
        c = _get_cache(f, method_args, argsp_v)
        if not _cache_exists(c):
            debug("cache miss for {0}({1})".format(f.__name__, *method_args))
            return_value, elapsed_time = _execute_func(f, *method_args, **method_kwargs)
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


def _salvarCache():
    salvarNovosDadosBanco()
