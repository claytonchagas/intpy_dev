import inspect
from functools import wraps
import time

from .data_access import get_cache_data, create_entry, salvarNovosDadosBanco
from .logger.log import debug

import threading
from . import CONSTANTES
from .banco import Banco
import os
def _get_cache(func, args, functionReturnList):
    print("CONSULTANDO O BANCO {0}({1})...".format(func.__name__, *args))

    #Opening connection with database for current running thread
    CONSTANTES.CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))

    c = get_cache_data(func.__name__, args, inspect.getsource(func))
    if not _cache_exists(c):
        debug("cache miss for {0}({1})".format(func.__name__, args))
    else:
        debug("cache hit for {0}({1})".format(func.__name__, args))
        functionReturnList.append(c)

    CONSTANTES.CONEXAO_BANCO.fecharConexao()
    print("CONSULTA AO BANCO {0}({1}) CONCLUÍDA!".format(func.__name__, *args))

def _cache_exists(cache):
    return cache is not None


def _cache_data(func, fun_args, fun_return, elapsed_time):
    debug("starting caching data for {0}({1})".format(func.__name__, fun_args))
    start = time.perf_counter()
    create_entry(func.__name__, fun_args, fun_return, inspect.getsource(func))
    end = time.perf_counter()
    debug("caching {0} took {1}".format(func.__name__, end - start))


def _execute_func(f, functionReturnList, method_args, method_kwargs, self=None,):
    print("EXECUTANDO A FUNÇÃO {0}({1})...".format(f.__name__, *method_args))
    
    start = time.perf_counter()
    result_value = f(self, *method_args, **method_kwargs) if self is not None else f(*method_args, **method_kwargs)
    """
    functionCode = inspect.getsource(f)
    startExecution = False
    for codeLine in functionCode:
        if(startExecution):
            exec()
        if(codeLine.startswith("def ")):
            startExecution = True

    """
    end = time.perf_counter()

    elapsed_time = end - start

    debug("{0} took {1} to run".format(f.__name__, elapsed_time))

    print("EXECUÇÃO FUNÇÃO {0}({1}) CONCLUÍDA!".format(f.__name__, *method_args))

    functionReturnList.append((result_value, elapsed_time))


"""
CÓDIGO ANTIGO
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
"""


def _method_call(f):
    @wraps(f)
    def wrapper(self, *method_args, **method_kwargs):
        debug("calling {0}".format(f.__name__))
        
        functionReturnList = []
        cacheSearchThread = threading.Thread(target=_get_cache, args=tuple([f, method_args, functionReturnList]))
        cacheSearchThread.start()
        methodExecutionThread = threading.Thread(target=_execute_func, args=tuple([f, functionReturnList, method_args, method_kwargs, self]))
        methodExecutionThread.start()

        print("inspect.getsource(f):", inspect.getsource(f))

        while True:
            if(len(functionReturnList) > 0):
                break
        
        print("functionReturnList:", functionReturnList)

        if(isinstance(functionReturnList[0], tuple)):
            _cache_data(f, method_args, functionReturnList[0][0], inspect.getsource(f))
            return functionReturnList[0][0]
        
        return functionReturnList[0]

    return wrapper


def _function_call(f):
    @wraps(f)
    def wrapper(*method_args, **method_kwargs):
        debug("calling {0}".format(f.__name__))

        functionReturnList = []
        cacheSearchThread = threading.Thread(target=_get_cache, args=tuple([f, method_args, functionReturnList]))
        cacheSearchThread.start()
        functionExecutionThread = threading.Thread(target=_execute_func, args=tuple([f, functionReturnList, method_args, method_kwargs]))
        functionExecutionThread.start()

        #print("inspect.getsource(f):", inspect.getsource(f))

        while True:
            if(len(functionReturnList) > 0):
                break
        
        print("functionReturnList:", functionReturnList)

        if(isinstance(functionReturnList[0], tuple)):
            _cache_data(f, method_args, functionReturnList[0][0], inspect.getsource(f))
            return functionReturnList[0][0]
        
        return functionReturnList[0]

    return wrapper

# obs
def _is_method(f):
    args = inspect.getfullargspec(f).args
    return bool(args and args[0] == 'self')


def deterministic(f):
    return _method_call(f) if _is_method(f) else _function_call(f)

def salvarCache():
    salvarNovosDadosBanco()