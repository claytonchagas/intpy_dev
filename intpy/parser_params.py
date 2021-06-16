import argparse
import sys


def usage_msg():
    return "\nIntPy's Python command line arguments help:\n\n\
To run your experiment with IntPy use:\n\
$ python "+str(sys.argv[0])+" program_arguments [-h] [-v version, --version version] [--no-cache]\n\n\
To run in the IntPy DEBUG mode use:\n\
$ DEBUG=True python "+str(sys.argv[0])+" program_arguments [-h] [-v version, --version version] [--no-cache]"


def get_params():
    versions = ['1d-ow', 'v021x', '1d-ad', 'v022x', '2d-ad', 'v023x', '2d-ad-t', 'v024x', '2d-ad-f', 'v025x', '2d-ad-ft', 'v026x', '2d-lz', 'v027x']

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
