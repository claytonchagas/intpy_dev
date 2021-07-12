import argparse
import sys


def usage_msg():
    return "\nIntPy's Python command line arguments help:\n\n\
To run your experiment with IntPy use:\n\
$ python "+str(sys.argv[0])+" program_arguments [-h] [-v version, --version version] [--no-cache]\n\n\
To run in the IntPy DEBUG mode use:\n\
$ DEBUG=True python "+str(sys.argv[0])+" program_arguments [-h] [-v version, --version version] [--no-cache]\n\n\
Glossary of the versions:\n\
    =>v01x             : original version with some bug fixes and instrumentation, all data are stored directly in the database.\n\
    =>1d-ow    or v021x: one dicionary (1d), only write (ow), 1st implementation of dictionary: new data is added to the dictionary only when cache miss occur and the function decorated with @deterministic is executed.\n\
    =>1d-ad    or v022x: one dicionary (1d), all data loaded at the begining (ad), 2nd implementation of dictionary (uses 1 dictionary): at the begining of the execution all the data cached is loaded to the dictonary before the user script starts to run.\n\
    =>2d-ad    or v023x: two dicionaries (2d), all data loaded at the begining (ad), 3rd implementation of dictionary (uses 2 dictionaries): at the begining of the execution all the data cached is loaded to the dictionary DATA_DICTIONARY before the user script starts to run. When cache miss occurs and a function decorated with @deterministic is processed, its result is stored in NEW_DATA_DICTIONARY. This way, only the elements of NEW_DATA_DICTIONARY are added to the database at the end of the execution.\n\
    =>2d-ad-t  or v024x: two dicionaries (2d), all data loaded at the begining with a thread (ad-t), 4th implementation of dictionary (uses 2 dictionaries): at the begining of the execution a thread is started to load all the data cached in the database to the dictionary DATA_DICTIONARY. When cache miss occurs and a function decorated with @deterministic is processed, its result is stored in NEW_DATA_DICTIONARY. Only the elements of NEW_DATA_DICTIONARY are added to the database at the end of the execution but it is possible that some elements in NEW_DATA_DICTIONARY are already in the database due to the concurrent execution of the experiment and the thread that populates DATA_DICTIONARY.\n\
    =>2d-ad-f  or v025x: two dicionaries (2d), all data loaded at the begining of a function(ad-f), 5th implementation of dictionary (uses 2 dictionaries): when @deterministic is executed a select query is created to the database to bring all results of the function decorated with @deterministic stored in the cache. A list of functions already inserted to the dictionary is maintained to avoid unecessary querys to the database. The results are then stored in the dictionary DATA_DICTIONARY. When cache miss occurs and a function decorated with @deterministic is processed, its result is stored in NEW_DATA_DICTIONARY. This way, only the elements of NEW_DATA_DICTIONARY are added to the database at the end of the execution.\n\
    =>2d-ad-ft or v026x: two dicionaries (2d), all data loaded at the begining of a function with a thread (ad-ft), 6th implementation of dictionary (uses 2 dictionaries): when @deterministic is executed a select query is created to the database to bring all results of the function decorated with @deterministic stored in the cache. A list of functions already inserted to the dictionary is maintained to avoid unecessary querys to the database. The results of the query are stored in the dictionary DATA_DICTIONARY by a thread. When cache miss occurs and a function decorated with @deterministic is processed, its result is stored in NEW_DATA_DICTIONARY. This way, only the elements of NEW_DATA_DICTIONARY are added to the database at the end of the execution.\n\
    =>2d-lz    or v027x: two dicionaries (2d), lazy mode (lz), 7th implementation of dictionary (uses 2 dictionaries): new data is added to DATA_DICTIONARY when cache hit occurs (LAZY approach) and new data is added to NEW_DATA_DICTIONARY when cache miss occur and the function decorated with @deterministic is executed."


def get_params():
    versions = ['v01x', '1d-ow', 'v021x', '1d-ad', 'v022x', '2d-ad', 'v023x', '2d-ad-t', 'v024x', '2d-ad-f', 'v025x', '2d-ad-ft', 'v026x', '2d-lz', 'v027x']

    intpy_arg_parser = argparse.ArgumentParser(usage=usage_msg())

    intpy_arg_parser.add_argument('args',
                                   metavar='program arguments',
                                   nargs='*',
                                   type=str, 
                                   help='program arguments')

    intpy_arg_parser.add_argument('-v',
                                  '--version',
                                   choices=versions,
                                   metavar='',
                                   nargs=1,
                                   type=str, 
                                   help='IntPy\'s mechanism version: choose one of the following options: '+', '.join(versions))

    intpy_arg_parser.add_argument('--no-cache',
                                  default=False,
                                  action="store_true",
                                  help='IntPy\'s disable cache')

    args = intpy_arg_parser.parse_args()

    argsp_v = args.version

    argsp_no_cache = args.no_cache

    return argsp_v, argsp_no_cache

"""
if argsp.version == ['1d-ow'] or argsp.version == ['v021x']:
    v_data_access = ".data_access_v021x_1d-ow"
elif argsp.version == ['1d-ad'] or argsp.version == ['v022x']:
    v_data_access = ".data_access_v022x_1d-ad"
elif argsp.version == ['2d-ad'] or argsp.version == ['v023x']:
    v_data_access = ".data_access_v023x_2d-ad"
elif argsp.version == ['2d-ad-t'] or argsp.version == ['v024x']:
    v_data_access = ".data_access_v024x_2d-ad-t"
elif argsp.version == ['2d-ad-f'] or argsp.version == ['v025x']:
    v_data_access = ".data_access_v025x_2d-ad-f"
elif argsp.version == ['2d-ad-ft'] or argsp.version == ['v026x']:
    v_data_access = ".data_access_v026x_2d-ad-ft"
elif argsp.version == ['2d-lz'] or argsp.version == ['v027x']:
    v_data_access = ".data_access_v027x_2d-lz"
else:
    v_data_access = ".data_access_v021x_1d-ow"
    """
