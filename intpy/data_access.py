import pickle
import hashlib
import os
import threading

from intpy.parser_params import get_params
from intpy.banco import Banco
from intpy.logger.log import debug

#from . import CONEXAO_BANCO

# Opening database connection and creating select query to the database
# to populate DATA_DICTIONARY
g_argsp_v, g_argsp_no_cache = get_params()
CONEXAO_BANCO = None
if(g_argsp_v != ['v01x']):
    CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))
DATA_DICTIONARY = {}
NEW_DATA_DICTIONARY = {}
FUNCTIONS_ALREADY_SELECTED_FROM_DB = []
CACHED_DATA_DICTIONARY_SEMAPHORE = threading.Semaphore()


def _save(fun_hash, fun_return):
    CONEXAO_BANCO.executarComandoSQLSemRetorno("INSERT OR IGNORE INTO CACHE(fun_hash, fun_return) VALUES (?, ?)", (fun_hash, str(fun_return)))


#Versão desenvolvida por causa do _save em salvarNovosDadosBanco para a v0.2.5.x e a v0.2.6.x, com o nome da função
#Testar se existe a sobrecarga
def _save_fun_name(fun_hash, fun_return, fun_name):
    CONEXAO_BANCO.executarComandoSQLSemRetorno("INSERT OR IGNORE INTO CACHE(fun_hash, fun_return, fun_name) VALUES (?, ?, ?)", (fun_hash, str(fun_return), fun_name))


def _get(id):
    return CONEXAO_BANCO.executarComandoSQLSelect("SELECT fun_return FROM CACHE WHERE fun_hash = ?", (id,))


#Versão desenvolvida por causa do _get_fun_name, que diferente do _get, recebe o nome da função ao invés do id, serve para a v0.2.5.x e a v0.2.6.x, que tem o nome da função
def _get_fun_name(fun_name):
    return CONEXAO_BANCO.executarComandoSQLSelect("SELECT fun_hash, fun_return FROM CACHE WHERE fun_name = ?", (fun_name,))


def _get_id(fun_args, fun_source):
    return hashlib.md5((str(fun_args) + fun_source).encode('utf')).hexdigest()


def _deserialize(data):
    return pickle.loads(data)


def _serialize(return_value):
    return pickle.dumps(return_value, protocol=pickle.HIGHEST_PROTOCOL)


def _get_cache_data_v01x(id):
    global CONEXAO_BANCO
    CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))
    list_fun_returns = _get(id)
    CONEXAO_BANCO.fecharConexao()
    return _deserialize(eval(list_fun_returns[0][0])) if len(list_fun_returns) == 1 else None


def _get_cache_data_v021x(id):
    #Nesta versão, DATA_DICTIONARY armazena os dados novos ainda não
    #persistidos no banco de dados
    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]
    list_fun_returns = _get(id)
    return _deserialize(eval(list_fun_returns[0][0])) if len(list_fun_returns) == 1 else None


def _get_cache_data_v022x(id):
    #Nesta versão, DATA_DICTIONARY armazena os dados novos ainda não
    #persistidos no banco de dados e os dados já persitidos no banco de dados
    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]
    return None


def _get_cache_data_v023x(id):
    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]    
    if(id in NEW_DATA_DICTIONARY):
        return NEW_DATA_DICTIONARY[id]
    return None


def _get_cache_data_v024x(id):
    with CACHED_DATA_DICTIONARY_SEMAPHORE:
        if(id in DATA_DICTIONARY):
            return DATA_DICTIONARY[id]
    if(id in NEW_DATA_DICTIONARY):
        return NEW_DATA_DICTIONARY[id]
    return None


def _get_cache_data_v025x(id, fun_name):
    if(fun_name in FUNCTIONS_ALREADY_SELECTED_FROM_DB):
        if(id in DATA_DICTIONARY):
            return DATA_DICTIONARY[id]
        if(id in NEW_DATA_DICTIONARY):
            #Nesta versão, os valores de NEW_DATA_DICTIONARY são a tupla
            #(retorno_da_funcao, nome_da_funcao)
            return NEW_DATA_DICTIONARY[id][0]
    else:
        list_cached_functions = _get_fun_name(fun_name)
        for cached_function in list_cached_functions:
            result = _deserialize(eval(cached_function[1]))
            if(result is None):
                continue
            else:
                DATA_DICTIONARY[cached_function[0]] = result

        FUNCTIONS_ALREADY_SELECTED_FROM_DB.append(fun_name)
        if(id in DATA_DICTIONARY):
            return DATA_DICTIONARY[id]
    return None

#This version doesn't make sense to be implemented in a version of IntPy
#that uses only the database
def _get_cache_data_v026x(id, fun_name):
    pass


#Comparável à versão v021x, mas com 2 dicionários
def _get_cache_data_v027x(id):
    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]
    if(id in NEW_DATA_DICTIONARY):
        return NEW_DATA_DICTIONARY[id]
    
    list_fun_returns = _get(id)
    result = _deserialize(eval(list_fun_returns[0][0])) if len(list_fun_returns) == 1 else None
    if(result is not None):
        DATA_DICTIONARY[id] = result
    return result


# Aqui misturam as versões v0.2.1.x a v0.2.7.x e v01x
def get_cache_data(fun_name, fun_args, fun_source, argsp_v):
    id = _get_id(fun_args, fun_source)

    if(argsp_v == ['v01x']):
        ret_get_cache_data_v01x = _get_cache_data_v01x(id)
        return ret_get_cache_data_v01x
    elif(argsp_v == ['1d-ow'] or argsp_v == ['v021x']):
        ret_get_cache_data_v021x = _get_cache_data_v021x(id)
        return ret_get_cache_data_v021x
    elif(argsp_v == ['1d-ad'] or argsp_v == ['v022x']):
        ret_get_cache_data_v022x = _get_cache_data_v022x(id)
        return ret_get_cache_data_v022x
    elif(argsp_v == ['2d-ad'] or argsp_v == ['v023x']):
        ret_get_cache_data_v023x = _get_cache_data_v023x(id)
        return ret_get_cache_data_v023x
    elif(argsp_v == ['2d-ad-t'] or argsp_v == ['v024x']):
        ret_get_cache_data_v024x = _get_cache_data_v024x(id)
        return ret_get_cache_data_v024x
    elif(argsp_v == ['2d-ad-f'] or argsp_v == ['v025x']):
        ret_get_cache_data_v025x = _get_cache_data_v025x(id, fun_name)
        return ret_get_cache_data_v025x
    elif(argsp_v == ['2d-ad-ft'] or argsp_v == ['v026x']):
        ret_get_cache_data_v026x = _get_cache_data_v026x(id, fun_name)
        return ret_get_cache_data_v026x
    elif(argsp_v == ['2d-lz'] or argsp_v == ['v027x']):
        ret_get_cache_data_v027x = _get_cache_data_v027x(id)
        return ret_get_cache_data_v027x


# Aqui misturam as versões v0.2.1.x a v0.2.7.x e v01x
def create_entry(fun_name, fun_args, fun_return, fun_source, argsp_v):
    id = _get_id(fun_args, fun_source)
    if argsp_v == ['v01x']:
        global CONEXAO_BANCO
        CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))
        debug("serializing return value from {0}".format(id))
        fun_return_serialized = _serialize(fun_return)
        debug("inserting reference in database")
        _save(id, fun_return_serialized)
        CONEXAO_BANCO.salvarAlteracoes()
        CONEXAO_BANCO.fecharConexao()

    elif(argsp_v == ['1d-ow'] or argsp_v == ['v021x'] or
        argsp_v == ['1d-ad'] or argsp_v == ['v022x']):
        DATA_DICTIONARY[id] = fun_return

    elif(argsp_v == ['2d-ad'] or argsp_v == ['v023x'] or 
        argsp_v == ['2d-ad-t'] or argsp_v == ['v024x'] or
        argsp_v == ['2d-lz'] or argsp_v == ['v027x']):
        NEW_DATA_DICTIONARY[id] = fun_return
    elif(argsp_v == ['2d-ad-f'] or argsp_v == ['v025x'] or
        argsp_v == ['2d-ad-ft'] or argsp_v == ['v026x']):
        NEW_DATA_DICTIONARY[id] = (fun_return, fun_name)


# Aqui misturam as versões v0.2.1.x a v0.2.7.x
def salvarNovosDadosBanco(argsp_v):
    if(argsp_v == ['1d-ow'] or argsp_v == ['v021x'] or
        argsp_v == ['1d-ad'] or argsp_v == ['v022x']):        
        for id in DATA_DICTIONARY:
            debug("serializing return value from {0}".format(id))
            fun_return_serialized = _serialize(DATA_DICTIONARY[id])
            debug("inserting reference in database")
            _save(id, fun_return_serialized)
    
    elif(argsp_v == ['2d-ad'] or argsp_v == ['v023x'] or
        argsp_v == ['2d-ad-t'] or argsp_v == ['v024x'] or
        argsp_v == ['2d-lz'] or argsp_v == ['v027x']):        
        for id in NEW_DATA_DICTIONARY:
            debug("serializing return value from {0}".format(id))
            fun_return_serialized = _serialize(NEW_DATA_DICTIONARY[id])
            debug("inserting reference in database")
            _save(id, fun_return_serialized)
    
    elif(argsp_v == ['2d-ad-f'] or argsp_v == ['v025x'] or
        argsp_v == ['2d-ad-ft'] or argsp_v == ['v026x']):
        for id in NEW_DATA_DICTIONARY:
            debug("serializing return value from {0}".format(id))
            fun_return_serialized = _serialize(NEW_DATA_DICTIONARY[id][0])
            debug("inserting reference in database")
            _save_fun_name(id, fun_return_serialized, NEW_DATA_DICTIONARY[id][1])

    CONEXAO_BANCO.salvarAlteracoes()
    CONEXAO_BANCO.fecharConexao()


if(g_argsp_v == ['1d-ad'] or g_argsp_v == ['v022x']
    or g_argsp_v == ['2d-ad'] or g_argsp_v == ['v023x']):
    def _populate_cached_data_dictionary():
        list_cached_functions = CONEXAO_BANCO.executarComandoSQLSelect("SELECT fun_hash, fun_return FROM CACHE")
        for cached_function in list_cached_functions:
            result = _deserialize(eval(cached_function[1]))
            if(result is None):
                continue
            else:
                DATA_DICTIONARY[cached_function[0]] = result
    _populate_cached_data_dictionary()
elif(g_argsp_v == ['2d-ad-t'] or g_argsp_v == ['v024x']):
    def _populate_cached_data_dictionary():
        db_connection = Banco(os.path.join(".intpy", "intpy.db"))
        list_cached_functions = db_connection.executarComandoSQLSelect("SELECT fun_hash, fun_return FROM CACHE")
        for cached_function in list_cached_functions:
            result = _deserialize(eval(cached_function[1]))
            if(result is None):
                continue
            else:
                with CACHED_DATA_DICTIONARY_SEMAPHORE:
                    DATA_DICTIONARY[cached_function[0]] = result
        db_connection.fecharConexao()
    load_cached_data_dictionary_thread = threading.Thread(target=_populate_cached_data_dictionary)
    load_cached_data_dictionary_thread.start()
