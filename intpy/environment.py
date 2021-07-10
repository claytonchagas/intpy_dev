import os
#import ctypes
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


def _folder_exists():
    return os.path.exists(FOLDER_NAME)


def _env_exists():
    return _folder_exists()


def init_env():
    debug("cheking if intpy environment exists")
    if _env_exists():
        debug("environment already exists")
        return

    debug("creating intpy environment")
    _create_folder()
