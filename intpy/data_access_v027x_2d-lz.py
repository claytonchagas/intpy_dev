import pickle
import re
import hashlib

from .logger.log import debug, error, warn
from .banco import Banco
import os

def _save(file_name):
    CONEXAO_BANCO.executarComandoSQLSemRetorno("INSERT OR IGNORE INTO CACHE(cache_file) VALUES ('{0}')".format(file_name))


def _get(id):
    return CONEXAO_BANCO.executarComandoSQLSelect("SELECT cache_file FROM CACHE WHERE cache_file = '{0}'".format(id))


def _remove(id):
    CONEXAO_BANCO.executarComandoSQLSemRetorno("DELETE FROM CACHE WHERE cache_file = '{0}';".format(id))


def _get_file_name(id):
    return "{0}.{1}".format(id, "ipcache")


def _get_id(fun_name, fun_args, fun_source):
    return hashlib.md5((fun_name + str(fun_args) + fun_source).encode('utf')).hexdigest()


def get_cache_data(fun_name, fun_args, fun_source):
    def deserialize(id):
        try:
            with open(".intpy/cache/{0}".format(_get_file_name(id)), 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError as e:
            warn("corrupt environment. Cache reference exists for {0} in database but there is no file for it in cache folder.\
 Have you deleted cache folder?".format(fun_name))
            autofix(id)
            return None
    
    ######print("CACHED_DATA_DICTIONARY ANTES:", CACHED_DATA_DICTIONARY)
    ######print("NEW_DATA_DICTIONARY:", NEW_DATA_DICTIONARY)


    id = _get_id(fun_name, fun_args, fun_source)
    
    #Checking if the result is stored in CACHED_DATA_DICTIONARY
    if(id in CACHED_DATA_DICTIONARY):
        return CACHED_DATA_DICTIONARY[id]

    #Checking if the result is stored in NEW_DATA_DICTIONARY
    if(id in NEW_DATA_DICTIONARY):
        return NEW_DATA_DICTIONARY[id]
    
    ######print("PESQUISANDO NO BANCO...")

    #Checking if the result is on database
    list_file_name = _get(_get_file_name(id))

    if(len(list_file_name) == 1):
        result = deserialize(id)
        
        if(result is not None):
            CACHED_DATA_DICTIONARY[id] = result

            ######print("CACHED_DATA_DICTIONARY DEPOIS:", CACHED_DATA_DICTIONARY)
        
        return result
    
    return None


def autofix(id):
    debug("starting autofix")
    debug("removing {0} from database".format(id))
    _remove(_get_file_name(id))
    debug("environment fixed")


def create_entry(fun_name, fun_args, fun_return, fun_source):
    id = _get_id(fun_name, fun_args, fun_source)
    NEW_DATA_DICTIONARY[id] = fun_return

def salvarNovosDadosBanco():
    def serialize(return_value, file_name):
        with open(".intpy/cache/{0}".format(_get_file_name(file_name)), 'wb') as file:
            return pickle.dump(return_value, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    for id in NEW_DATA_DICTIONARY:
        debug("serializing return value from {0}".format(id))
        serialize(NEW_DATA_DICTIONARY[id], id)

        debug("inserting reference in database")
        _save(_get_file_name(id))

    CONEXAO_BANCO.salvarAlteracoes()
    CONEXAO_BANCO.fecharConexao()

CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))
CACHED_DATA_DICTIONARY = {}
NEW_DATA_DICTIONARY = {}
