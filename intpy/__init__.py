from .environment import init_env

init_env()

#This import is necessary because when it is executed, a select query to
#the database is started an all the data is brought and included in the
#DATA_DICTIONARY defined at that file
from .data_access_v022x_1d-ad import *