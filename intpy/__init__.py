import os
from .db import DB
from .environment import init_env

init_env()

CONN_DB = DB(os.path.join(".intpy", "intpy.db"))