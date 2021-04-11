import os
from .banco import Banco
from .environment import init_env
import threading

init_env()

CONSTANTES = threading.local()
CONSTANTES.CONEXAO_BANCO = Banco(os.path.join(".intpy", "intpy.db"))