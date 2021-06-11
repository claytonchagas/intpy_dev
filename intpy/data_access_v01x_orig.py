import pickle
import sqlite3
import re
import hashlib

from .environment import init_env
from .logger.log import debug, error, warn


def _create_conn():
    return sqlite3.connect('.intpy/intpy.db')


def _close_conn(conn):
    conn.close()


def _exec_stmt(stmt):
    conn = _create_conn()
    conn.execute(stmt)
    conn.commit()
    conn.close()


def _exec_stmt_return(stmt):
    conn = _create_conn()
    cursor = conn.execute(stmt)
    return cursor.fetchone()


def _save(file_name):
    _exec_stmt("INSERT INTO CACHE(cache_file) VALUES ('{0}')".format(file_name))


def _get(id):
    return _exec_stmt_return("SELECT cache_file FROM CACHE WHERE cache_file = '{0}'".format(id))


def _remove(id):
    _exec_stmt("DELETE FROM CACHE WHERE cache_file = '{0}';".format(id))


def _get_file_name(id):
    return "{0}.{1}".format(id, "ipcache")


def _get_id(fun_name, fun_args, fun_source):
    return hashlib.md5((fun_name + str(fun_args) + fun_source).encode('utf')).hexdigest()


@init_env
def get_cache_data(fun_name, fun_args, fun_source):
    id = _get_id(fun_name, fun_args, fun_source)
    file_name = _get(_get_file_name(id))

    def deserialize(id):
        try:
            with open(".intpy/cache/{0}".format(_get_file_name(id)), 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError as e:
            warn("corrupt environment. Cache reference exists for {0} in database but there is no file for it in cache folder.\
 Have you deleted cache folder?".format(fun_name))
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

    def serialize(return_value, file_name):
        with open(".intpy/cache/{0}".format(_get_file_name(file_name)), 'wb') as file:
            return pickle.dump(return_value, file, protocol=pickle.HIGHEST_PROTOCOL)

    debug("serializing return value from {0}".format(fun_name))
    serialize(fun_return, id)

    debug("inserting reference in database")
    _save(_get_file_name(id))
