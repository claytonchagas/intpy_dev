import pickle
import re
import hashlib
import threading

from .logger.log import debug, error, warn
from .banco import Banco
import os

def _save(file_name, fun_name):
    CONEXAO_BANCO.executarComandoSQLSemRetorno("INSERT OR IGNORE INTO CACHE(cache_file, fun_name) VALUES ('{0}', '{1}')".format(file_name, fun_name))


def _get(fun_name):
    return CONEXAO_BANCO.executarComandoSQLSelect("SELECT cache_file FROM CACHE WHERE fun_name = '{0}'".format(fun_name))


def _remove(id):
    CONEXAO_BANCO.executarComandoSQLSemRetorno("DELETE FROM CACHE WHERE cache_file = '{0}';".format(id))


def _get_file_name(id):
    return "{0}.{1}".format(id, "ipcache")


def _get_id(fun_name, fun_args, fun_source):
    return hashlib.md5((fun_name + str(fun_args) + fun_source).encode('utf')).hexdigest()


def add_new_data_to_CACHED_DATA_DICTIONARY(list_file_names):
    for file_name in list_file_names:
        file_name = file_name[0].replace(".ipcache", "")
        
        result = deserialize(file_name)
        if(result is None):
            continue
        else:
            CACHED_DATA_DICTIONARY[file_name] = result

    print("CACHED_DATA_DICTIONARY DEPOIS:", CACHED_DATA_DICTIONARY)


def get_cache_data(fun_name, fun_args, fun_source):

    print("NEW_DATA_DICTIONARY:", NEW_DATA_DICTIONARY)
    print("CACHED_DATA_DICTIONARY ANTES:", CACHED_DATA_DICTIONARY)
    

    id = _get_id(fun_name, fun_args, fun_source)

    #Checking if the results of this function were already selected from
    #the database and inserted on the dictionary CACHED_DATA_DICTIONARY
    if(fun_name in FUNCTIONS_ALREADY_SELECTED_FROM_DB):
        #Checking if the result is saved in the cache
        if(id in CACHED_DATA_DICTIONARY):
            return CACHED_DATA_DICTIONARY[id]

        #Checking if the result was already processed at this execution
        if(id in NEW_DATA_DICTIONARY):
            return NEW_DATA_DICTIONARY[id][0]
    
    else:
        #Creating a select query to add to CACHED_DATA_DICTIONARY all data
        #related to the function fun_name
        FUNCTIONS_ALREADY_SELECTED_FROM_DB.append(fun_name)
        id_file_name = _get_file_name(id)
        
        list_file_names = _get(fun_name)
        for file_name in list_file_names:
            if(file_name[0] == id_file_name):
                thread = threading.Thread(target=add_new_data_to_CACHED_DATA_DICTIONARY, args=(list_file_names,))
                thread.start()

                file_name = file_name[0].replace(".ipcache", "")
                return deserialize(file_name)
        
        thread = threading.Thread(target=add_new_data_to_CACHED_DATA_DICTIONARY, args=(list_file_names,))
        thread.start()

    return None


def autofix(id):
    debug("starting autofix")
    debug("removing {0} from database".format(id))
    _remove(_get_file_name(id))
    debug("environment fixed")


def create_entry(fun_name, fun_args, fun_return, fun_source):
    id = _get_id(fun_name, fun_args, fun_source)
    NEW_DATA_DICTIONARY[id] = (fun_return, fun_name)

def salvarNovosDadosBanco():
    def serialize(return_value, file_name):
        with open(".intpy/cache/{0}".format(_get_file_name(file_name)), 'wb') as file:
            return pickle.dump(return_value, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    for id in NEW_DATA_DICTIONARY:
        debug("serializing return value from {0}".format(id))
        serialize(NEW_DATA_DICTIONARY[id][0], id)

        debug("inserting reference in database")
        _save(_get_file_name(id), NEW_DATA_DICTIONARY[id][1])

    CONEXAO_BANCO.salvarAlteracoes()
    CONEXAO_BANCO.fecharConexao()

def deserialize(id):
    try:
        with open(".intpy/cache/{0}".format(_get_file_name(id)), 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError as e:
        warn("corrupt environment. Cache reference exists for a function in database but there is no file for it in cache folder.\
Have you deleted cache folder?")
        autofix(id)
        return None

#Opening database connection and creating dictionaries
CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))
CACHED_DATA_DICTIONARY = {}
FUNCTIONS_ALREADY_SELECTED_FROM_DB = []
NEW_DATA_DICTIONARY = {}
