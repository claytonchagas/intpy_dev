import pickle
import re
import hashlib

from .logger.log import debug, error, warn

from . import CONN_DB

DICT_NEW_DATA = {}

def _save(file_name):
    CONN_DB.executeCmdSQLNoReturn("INSERT INTO CACHE(cache_file) VALUES ('{0}')".format(file_name))


def _get(id):
    return CONN_DB.executeCmdSQLSelect("SELECT cache_file FROM CACHE WHERE cache_file = '{0}'".format(id))


def _remove(id):
    CONN_DB.executeCmdSQLNoReturn("DELETE FROM CACHE WHERE cache_file = '{0}';".format(id))


def _get_file_name(id):
    return "{0}.{1}".format(id, "ipcache")


def _get_id(fun_name, fun_args, fun_source):
    return hashlib.md5((fun_name + str(fun_args) + fun_source).encode('utf')).hexdigest()


def get_cache_data(fun_name, fun_args, fun_source):
    id = _get_id(fun_name, fun_args, fun_source)
    return get_cache_data_by_id(id)

def get_cache_data_by_id(id):
    #Verificando se há dados salvos em "DICT_NEW_DATA"
    if(id in DICT_NEW_DATA):
        return DICT_NEW_DATA[id]
    
    #Verificando se há dados salvos no banco
    list_file_name = _get(_get_file_name(id))
    file_name = None
    if(len(list_file_name) == 1):
        file_name = list_file_name[0]

    def deserialize(id):
        try:
            with open(".intpy/cache/{0}".format(_get_file_name(id)), 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError as e:
            warn("corrupt environment. Cache reference exists for a function in database but there is no file for it in cache folder.\
 Have you deleted cache folder?")
            autofix(id)
            return None

    return deserialize(id) if file_name is not None else None


def autofix(id):
    debug("starting autofix")
    debug("removing {0} from database".format(id))
    _remove(_get_file_name(id))
    debug("environment fixed")


def create_entry(fun_name, fun_args, fun_return, fun_source):
    id = _get_id(fun_name, fun_args, fun_source)
    DICT_NEW_DATA[id] = fun_return

def saveNewDataDB():
    def serialize(return_value, file_name):
        with open(".intpy/cache/{0}".format(_get_file_name(file_name)), 'wb') as file:
            return pickle.dump(return_value, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    for i in range(len(DICT_NEW_DATA)):
        id =  list(DICT_NEW_DATA.keys())[0]
        returnValue = DICT_NEW_DATA[id]

        DICT_NEW_DATA.pop(id)
        if(get_cache_data_by_id(id)):
            continue
        
        debug("serializing return value from {0}".format(id))
        serialize(returnValue, id)

        debug("inserting reference in database")
        _save(_get_file_name(id))

    CONN_DB.saveChanges()
    CONN_DB.closeConection()