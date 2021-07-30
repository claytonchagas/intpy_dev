import pickle
import hashlib
import os, os.path
import threading

from intpy.parser_params import get_params
from intpy.logger.log import debug, warn

#from . import CONEXAO_BANCO

# Opening database connection and creating select query to the database
# to populate DATA_DICTIONARY
g_argsp_v, g_argsp_no_cache = get_params()

DATA_DICTIONARY = {}
NEW_DATA_DICTIONARY = {}
FUNCTIONS_ALREADY_SELECTED_FROM_CACHE = []
CACHED_DATA_DICTIONARY_SEMAPHORE = threading.Semaphore()


def _save(return_value, file_name):
    _serialize(return_value, file_name)


#Versão desenvolvida por causa do _save em salvarNovosDadosBanco para a v0.2.5.x e a v0.2.6.x, com o nome da função
#Testar se existe a sobrecarga
def _save_fun_name(return_value, fun_name, file_name):
    _serialize_fun_name(return_value, fun_name, file_name)


def _get(id):
    return _deserialize(id)


#Versão desenvolvida por causa do _get_fun_name, que diferente do _get, recebe o nome da função ao invés do id, serve para a v0.2.5.x e a v0.2.6.x, que tem o nome da função
def _get_fun_name(fun_name):
    return _deserialize_fun_name(fun_name)


def _get_id(fun_args, fun_source):
    return hashlib.md5((str(fun_args) + fun_source).encode('utf')).hexdigest()


def _get_file_name(id):
    return "{0}.{1}".format(id, "ipcache")


def _deserialize(id):
    try:
        with open(".intpy/{0}".format(_get_file_name(id)), 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError as e:
        return None


def _deserialize_fun_name(fun_name):
    deserialized_data = {}
    folder_path = ".intpy/{0}".format(fun_name)
    if(not os.path.exists(folder_path)):
        return deserialized_data
    for element in os.listdir(folder_path):
        element_path = ".intpy/{0}/{1}".format(fun_name, element)
        if(os.path.isfile(element_path)):
            with open(element_path, 'rb') as file:
                deserialized_data[element.replace(".ipcache", "")] = pickle.load(file)
    return deserialized_data


def _deserialize_fun_name_id(fun_name, id):
    try:
        with open(".intpy/{0}/{1}".format(fun_name, _get_file_name(id)), 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError as e:
        return None


def _serialize(return_value, file_name):
    with open(".intpy/{0}".format(_get_file_name(file_name)), 'wb') as file:
        return pickle.dump(return_value, file, protocol=pickle.HIGHEST_PROTOCOL)


def _serialize_fun_name(return_value, fun_name, file_name):
    folder_path = ".intpy/{0}".format(fun_name)
    if(not os.path.exists(folder_path)):
        os.mkdir(folder_path)
    with open(".intpy/{0}/{1}".format(fun_name, _get_file_name(file_name)), 'wb') as file:
        return pickle.dump(return_value, file, protocol=pickle.HIGHEST_PROTOCOL)


def _get_cache_data_v01x(id):
    return _get(id)


def _get_cache_data_v021x(id):
    #Nesta versão, DATA_DICTIONARY armazena os dados novos ainda não
    #persistidos no sistema de arquivos
    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]
    return _get(id)


def _get_cache_data_v022x(id):
    #Nesta versão, DATA_DICTIONARY armazena os dados novos ainda não
    #persistidos no sistema de arquivos e os dados já persitidos no
    #sistema de arquivos
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
    if(fun_name in FUNCTIONS_ALREADY_SELECTED_FROM_CACHE):
        if(id in DATA_DICTIONARY):
            return DATA_DICTIONARY[id]
        if(id in NEW_DATA_DICTIONARY):
            #Nesta versão, os valores de NEW_DATA_DICTIONARY são a tupla
            #(retorno_da_funcao, nome_da_funcao)
            return NEW_DATA_DICTIONARY[id][0]
    else:
        deserialized_data = _get_fun_name(fun_name)
        DATA_DICTIONARY.update(deserialized_data)
        FUNCTIONS_ALREADY_SELECTED_FROM_CACHE.append(fun_name)
        if(id in DATA_DICTIONARY):
            return DATA_DICTIONARY[id]
    return None


def _get_cache_data_v026x(id, fun_name):
    if(fun_name in FUNCTIONS_ALREADY_SELECTED_FROM_CACHE):
        with CACHED_DATA_DICTIONARY_SEMAPHORE:
            if(id in DATA_DICTIONARY):
                return DATA_DICTIONARY[id]
        if(id in NEW_DATA_DICTIONARY):
            #Nesta versão, os valores de NEW_DATA_DICTIONARY são a tupla
            #(retorno_da_funcao, nome_da_funcao)
            return NEW_DATA_DICTIONARY[id][0]
    else:
        FUNCTIONS_ALREADY_SELECTED_FROM_CACHE.append(fun_name)   
        thread = threading.Thread(target=add_new_data_to_CACHED_DATA_DICTIONARY, args=(fun_name,))
        thread.start()
        return _deserialize_fun_name_id(fun_name, id)
    return None


#Comparável à versão v021x, mas com 2 dicionários
def _get_cache_data_v027x(id):
    if(id in DATA_DICTIONARY):
        return DATA_DICTIONARY[id]
    if(id in NEW_DATA_DICTIONARY):
        return NEW_DATA_DICTIONARY[id]
    
    result = _get(id)
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


def add_new_data_to_CACHED_DATA_DICTIONARY(fun_name):        
    deserialized_data = _get_fun_name(fun_name)
    with CACHED_DATA_DICTIONARY_SEMAPHORE:
        DATA_DICTIONARY.update(deserialized_data)
    
 
# Aqui misturam as versões v0.2.1.x a v0.2.7.x e v01x
def create_entry(fun_name, fun_args, fun_return, fun_source, argsp_v):
    id = _get_id(fun_args, fun_source)
    if argsp_v == ['v01x']:
        debug("serializing return value from {0}".format(id))
        _save(fun_return, id)
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
            _save(DATA_DICTIONARY[id], id)
    
    elif(argsp_v == ['2d-ad'] or argsp_v == ['v023x'] or
        argsp_v == ['2d-ad-t'] or argsp_v == ['v024x'] or
        argsp_v == ['2d-lz'] or argsp_v == ['v027x']):
        for id in NEW_DATA_DICTIONARY:
            debug("serializing return value from {0}".format(id))
            _save(NEW_DATA_DICTIONARY[id], id)
    
    elif(argsp_v == ['2d-ad-f'] or argsp_v == ['v025x'] or
        argsp_v == ['2d-ad-ft'] or argsp_v == ['v026x']):
        for id in NEW_DATA_DICTIONARY:
            debug("serializing return value from {0}".format(id))
            _save_fun_name(NEW_DATA_DICTIONARY[id][0], NEW_DATA_DICTIONARY[id][1], id)


if(g_argsp_v == ['1d-ad'] or g_argsp_v == ['v022x']
    or g_argsp_v == ['2d-ad'] or g_argsp_v == ['v023x']):
    def _populate_cached_data_dictionary():
        for element in os.listdir(".intpy/"):
            element = element.replace(".ipcache", "")
            result = _get(element)
            if(result is None):
                continue
            else:
                DATA_DICTIONARY[element] = result
    _populate_cached_data_dictionary()
elif(g_argsp_v == ['2d-ad-t'] or g_argsp_v == ['v024x']):
    def _populate_cached_data_dictionary():
        for element in os.listdir(".intpy/"):
            element = element.replace(".ipcache", "")
            result = _get(element)
            if(result is None):
                continue
            else:
                with CACHED_DATA_DICTIONARY_SEMAPHORE:
                    DATA_DICTIONARY[element] = result
    load_cached_data_dictionary_thread = threading.Thread(target=_populate_cached_data_dictionary)
    load_cached_data_dictionary_thread.start()
