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

def _get_cache_serial(func, args):
    ######print("CONSULTANDO O BANCO {0}({1}) SERIALMENTE...".format(func.__name__, args))
    fun_source = get_source_code_executed(func, USER_SCRIPT_GRAPH)
    c = get_cache_data(args, fun_source)
    ######print("CONSULTA AO BANCO {0}({1}) SERIALMENTE CONCLUÍDA!".format(func.__name__, args))
    return c


def _get_cache(func, args, queue):
    ######print("CONSULTANDO O BANCO {0}({1})...".format(func.__name__, args))

    #Opening connection with database for current running process
    CONN_DB = DB(os.path.join(".intpy", "intpy.db"))

    fun_source = get_source_code_executed(func, USER_SCRIPT_GRAPH)
    c = get_cache_data(args, fun_source)
    if not _cache_exists(c):
        debug("cache miss for {0}({1})".format(func.__name__, args))
    else:
        debug("cache hit for {0}({1})".format(func.__name__, args))
        queue.put(c)

    CONN_DB.closeConection()
    ######print("CONSULTA AO BANCO {0}({1}) CONCLUÍDA!".format(func.__name__, args))

def _cache_exists(cache):
    return cache is not None


def _cache_data(func, fun_args, fun_return, elapsed_time):
    debug("starting caching data for {0}({1})".format(func.__name__, fun_args))
    start = time.perf_counter()
    fun_source = get_source_code_executed(func, USER_SCRIPT_GRAPH)
    create_entry(fun_args, fun_return, fun_source)
    end = time.perf_counter()
    debug("caching {0} took {1}".format(func.__name__, end - start))

def _execute_func_serial(f, method_args, method_kwargs, self=None,):
    ######print("EXECUTANDO A FUNÇÃO {0}({1}) SERIALMENTE...".format(f.__name__, method_args))
    
    start = time.perf_counter()
    result_value = f(self, *method_args, **method_kwargs) if self is not None else f(*method_args, **method_kwargs)
    end = time.perf_counter()

    elapsed_time = end - start

    debug("{0} took {1} to run".format(f.__name__, elapsed_time))

    ######print("EXECUÇÃO FUNÇÃO {0}({1}) SERIALMENTE CONCLUÍDA!".format(f.__name__, method_args))

    return (result_value, elapsed_time)


def _execute_func(f, queue, method_args, method_kwargs, self=None,):
    ######print("EXECUTANDO A FUNÇÃO {0}({1})...".format(f.__name__, method_args))
    
    start = time.perf_counter()
    result_value = f(self, *method_args, **method_kwargs) if self is not None else f(*method_args, **method_kwargs)
    end = time.perf_counter()

    elapsed_time = end - start

    debug("{0} took {1} to run".format(f.__name__, elapsed_time))

    queue.put((result_value, elapsed_time, DICT_NEW_DATA))

    ######print("EXECUÇÃO FUNÇÃO {0}({1}) CONCLUÍDA!".format(f.__name__, method_args))


def _method_call(f):
    @wraps(f)
    def wrapper(self, *method_args, **method_kwargs):
        debug("calling {0}".format(f.__name__))
        
        if(multiprocessing.parent_process() is None):
            #Parallel execution
            queue = multiprocessing.Queue()
            cacheSearchProcess = multiprocessing.Process(target=_get_cache, args=tuple([f, method_args, queue]))
            cacheSearchProcess.start()
            methodExecutionProcess = multiprocessing.Process(target=_execute_func, args=tuple([f, queue, method_args, method_kwargs, self]))
            methodExecutionProcess.start()

            processReturn = queue.get()
            
            ######print("processReturn:", processReturn)

            if(isinstance(processReturn, tuple)):
                cacheSearchProcess.terminate()
                _cache_data(f, method_args, processReturn[0], processReturn[1])
                DICT_NEW_DATA.update(processReturn[2])
                return processReturn[0]
            else:
                #In this case, the cacheSearchProcess executed faster than the functionExecutionProcess
                #Stopping functionExecutionProcess
                ######print("APAGANDO PROCESSO DA FUNÇÃO {0}({1})...".format(f.__name__, method_args))
                methodExecutionProcess.terminate()
            
            return processReturn

        else:
            #Serialized execution
            c = _get_cache_serial(f, method_args)
            if not _cache_exists(c):
                debug("cache miss for {0}({1})".format(f.__name__, *method_args))
                return_value, elapsed_time = _execute_func_serial(f, method_args, method_kwargs, self)
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


        """
        print("f.__name__: " + f.__name__)
        for item in inspect.getmembers(f):
            if(item[0] == "__qualname__"):
                print("inspect.getmembers(f).__qualname__: ", item)
        print("source_code_executed:\n" + get_source_code_executed(f, USER_SCRIPT_GRAPH))
        print("\n")
        """        

        
        if(multiprocessing.parent_process() is None):
            #Parallel execution
            queue = multiprocessing.Queue()
            cacheSearchProcess = multiprocessing.Process(target=_get_cache, args=tuple([f, method_args, queue]))
            cacheSearchProcess.start()
            functionExecutionProcess = multiprocessing.Process(target=_execute_func, args=tuple([f, queue, method_args, method_kwargs]))
            functionExecutionProcess.start()

            processReturn = queue.get()
            
            ######print("processReturn:", processReturn)

            if(isinstance(processReturn, tuple)):
                cacheSearchProcess.terminate()
                _cache_data(f, method_args, processReturn[0], processReturn[1])
                DICT_NEW_DATA.update(processReturn[2])
                return processReturn[0]
            else:
                #In this case, the cacheSearchProcess executed faster than the functionExecutionProcess
                #Stopping functionExecutionProcess
                ######print("APAGANDO PROCESSO DA FUNÇÃO {0}({1})...".format(f.__name__, method_args))
                functionExecutionProcess.terminate()
            
            return processReturn

        else:
            #Serialized execution
            c = _get_cache_serial(f, method_args)
            if not _cache_exists(c):
                debug("cache miss for {0}({1})".format(f.__name__, *method_args))
                return_value, elapsed_time = _execute_func_serial(f, method_args, method_kwargs)
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
    user_script_ast = python_code_to_AST(user_script_path)
    
    if(user_script_path is None):
        raise RuntimeError

    #Generating function_graph for the user script
    function_class_method_searcher = FunctionClassMethodSearcher(user_script_ast)
    function_class_method_searcher.search_for_functions_classes_and_methods()
    
    function_graph_creator = FunctionGraphCreator(user_script_ast,
                                                function_class_method_searcher.functions)
    function_graph_creator.generate_function_graph()

    global USER_SCRIPT_GRAPH
    USER_SCRIPT_GRAPH = function_graph_creator.function_graph

    #########DEBUG###########
    dictionary = function_class_method_searcher.functions
    #dictionary.update(function_class_method_searcher.instance_methods)
    #dictionary.update(function_class_method_searcher.class_methods)
    print("dictionary:", dictionary)
    USER_SCRIPT_GRAPH.print_graph(dictionary)
    #########################


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