import os
#import ctypes
from .banco import Banco

from intpy.logger.log import debug

FOLDER_NAME = ".intpy"
HIDDEN = 0x02


def _create_folder():
    debug("creating .intpy folder")
    if _folder_exists():
        debug(".intpy folder already exists")
        return

    os.makedirs(FOLDER_NAME)
    #ctypes.windll.kernel32.SetFileAttributesW(FOLDER_NAME, HIDDEN)


def _create_database():
    debug("creating database")
    if _db_exists():
        debug("database already exists")
        return

    _create_table()


def _create_table():
    debug("creating table")
    conexaoBanco = Banco('.intpy/intpy.db')
    stmt = "CREATE TABLE IF NOT EXISTS CACHE (\
    id INTEGER PRIMARY KEY AUTOINCREMENT,\
    fun_hash TEXT UNIQUE NOT NULL,\
    fun_return TEXT NOT NULL,\
    fun_name TEXT\
    );"
    conexaoBanco.executarComandoSQLSemRetorno(stmt)
    conexaoBanco.fecharConexao()


def _db_exists():
    return os.path.isfile('.intpy/intpy.db')


def _folder_exists():
    return os.path.exists(FOLDER_NAME)


def _env_exists():
    return _folder_exists() and _db_exists()


def init_env():
    debug("cheking if intpy environment exists")
    if _env_exists():
        debug("environment already exists")
        return

    debug("creating intpy environment")
    _create_folder()
    _create_database()
