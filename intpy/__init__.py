#import os
#from .banco import Banco
#from .db import DB
from .environment import init_env

init_env()
#CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))
#CONN_DB = DB(os.path.join(".intpy", "intpy.db"))