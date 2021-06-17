import pickle
import hashlib
import os

from intpy.banco import Banco
from intpy.logger.log import debug, warn

#from . import CONEXAO_BANCO

# Opening database connection and creating select query to the database
# to populate DATA_DICTIONARY
CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))


def _save(file_name):
    CONEXAO_BANCO.executarComandoSQLSemRetorno(
        "INSERT OR IGNORE INTO CACHE(cache_file) VALUES ('{0}')".format(file_name))


def _get(id):
    return CONEXAO_BANCO.executarComandoSQLSelect("SELECT cache_file FROM CACHE WHERE cache_file = '{0}'".format(id))


def _remove(id):
    CONEXAO_BANCO.executarComandoSQLSemRetorno(
        "DELETE FROM CACHE WHERE cache_file = '{0}';".format(id))


def _get_file_name(id):
    return "{0}.{1}".format(id, "ipcache")


def _get_id(fun_name, fun_args, fun_source):
    return hashlib.md5((fun_name + str(fun_args) + fun_source).encode('utf')).hexdigest()


DATA_DICTIONARY = {}

NEW_DATA_DICTIONARY = {}


def _get_cache_data_v021x(id):
    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]

    list_file_name = _get(_get_file_name(id))
    file_name = None
    if(len(list_file_name) == 1):
        file_name = list_file_name[0]

    return _deserialize(id) if file_name is not None else None


def _get_cache_data_v022x(id):
    list_of_ipcache_files = CONEXAO_BANCO.executarComandoSQLSelect(
        "SELECT cache_file FROM CACHE")
    for ipcache_file in list_of_ipcache_files:
        ipcache_file = ipcache_file[0].replace(".ipcache", "")

        result = _deserialize(ipcache_file)
        if(result is None):
            continue
        else:
            DATA_DICTIONARY[ipcache_file] = result

    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]

    return None


def _get_cache_data_v023x(id):
    list_of_ipcache_files = CONEXAO_BANCO.executarComandoSQLSelect(
        "SELECT cache_file FROM CACHE")
    for ipcache_file in list_of_ipcache_files:
        ipcache_file = ipcache_file[0].replace(".ipcache", "")

        result = _deserialize(ipcache_file)
        if(result is None):
            continue
        else:
            DATA_DICTIONARY[ipcache_file] = result

    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]
    
    if(id in NEW_DATA_DICTIONARY):
        return NEW_DATA_DICTIONARY[id]

    return None


# Aqui mistura v0.2.1.x e v0.2.2.x
def get_cache_data(fun_name, fun_args, fun_source, argsp_v):
    id = _get_id(fun_name, fun_args, fun_source)

    if argsp_v == ['1d-ow'] or argsp_v == ['v021x']:
        ret_get_cache_data_v021x = _get_cache_data_v021x(id)
        return ret_get_cache_data_v021x
    elif argsp_v == ['1d-ad'] or argsp_v == ['v022x']:
        ret_get_cache_data_v022x = _get_cache_data_v022x(id)
        return ret_get_cache_data_v022x
    elif argsp_v == ['2d-ad'] or argsp_v == ['v023x']:
        ret_get_cache_data_v023x = _get_cache_data_v023x(id)
        return ret_get_cache_data_v023x

"""
    if argsp_v == ['1d-ad'] or argsp_v == ['v022x']:
        list_of_ipcache_files = CONEXAO_BANCO.executarComandoSQLSelect("SELECT cache_file FROM CACHE")
        for ipcache_file in list_of_ipcache_files:
            ipcache_file = ipcache_file[0].replace(".ipcache", "")
        
            result = _deserialize(ipcache_file)
            if(result is None):
                continue
            else:
                DATA_DICTIONARY[ipcache_file] = result


    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]
    
    if argsp_v == ['1d-ad'] or argsp_v == ['v022x']:
        return None
    elif argsp_v == ['1d-ow'] or argsp_v == ['v021x']:
        list_file_name = _get(_get_file_name(id))
        file_name = None
        if(len(list_file_name) == 1):
            file_name = list_file_name[0]
        return _deserialize(id) if file_name is not None else None
###COMPARAR, COMPLETAR, TESTAR
"""


def _deserialize(id):
    try:
        with open(".intpy/cache/{0}".format(_get_file_name(id)), 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError as e:
        warn("corrupt environment. Cache reference exists for a function in database but there is no file for it in cache folder.\
Have you deleted cache folder?")
        _autofix(id)
        return None


def _autofix(id):
    debug("starting autofix")
    debug("removing {0} from database".format(id))
    _remove(_get_file_name(id))
    debug("environment fixed")


def create_entry(fun_name, fun_args, fun_return, fun_source, argsp_v):
    id = _get_id(fun_name, fun_args, fun_source)
    if argsp_v == ['1d-ow'] or argsp_v == ['v021x'] or argsp_v == ['1d-ow'] or argsp_v == ['v021x']:
        DATA_DICTIONARY[id] = fun_return
    elif argsp_v == ['2d-ad'] or argsp_v == ['v023x']:
        NEW_DATA_DICTIONARY[id] = fun_return


def salvarNovosDadosBanco(argsp_v):
    def _serialize(return_value, file_name):
        with open(".intpy/cache/{0}".format(_get_file_name(file_name)), 'wb') as file:
            return pickle.dump(return_value, file, protocol=pickle.HIGHEST_PROTOCOL)

    if argsp_v == ['1d-ow'] or argsp_v == ['v021x'] or argsp_v == ['1d-ow'] or argsp_v == ['v021x']:
        for id in DATA_DICTIONARY:
            debug("serializing return value from {0}".format(id))
            _serialize(DATA_DICTIONARY[id], id)

            debug("inserting reference in database")
            _save(_get_file_name(id))
    
    elif argsp_v == ['2d-ad'] or argsp_v == ['v023x']:
        for id in NEW_DATA_DICTIONARY:
            debug("serializing return value from {0}".format(id))
            _serialize(NEW_DATA_DICTIONARY[id], id)

            debug("inserting reference in database")
            _save(_get_file_name(id))

    CONEXAO_BANCO.salvarAlteracoes()
    CONEXAO_BANCO.fecharConexao()
