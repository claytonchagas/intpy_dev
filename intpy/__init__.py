import os
from .db import DB
from .environment import init_env
import threading

init_env()

CONSTANTS = threading.local()
CONSTANTS.CONN_DB = DB(os.path.join(".intpy", "intpy.db"))