import os
from .banco import Banco
from .environment import init_env

init_env()
CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))