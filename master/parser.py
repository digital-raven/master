""" Main argument parser.
"""

import argparse
import sys

from master import __version__


def print_version():
    class printVersion(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            print(__version__)
            sys.exit(0)
    return printVersion


def create_parser():
    """ Create main parser.

    Returns:
        Reference to the parser. Parse main command line args with
            parser.parse_args().
    """
    parser = argparse.ArgumentParser(
        prog='master',
        description=(
            'A command-line project manager. Run "master" with no '
            'arguments to perform first-time setup.'))

    parser.add_argument(
        '--config',
        help='Select custom configuration file.')

    parser.add_argument(
        '--root', help='Specify a custom root dir to operate on.')

    parser.add_argument(
        '--version', nargs=0, help='Print the version of master and exit.',
        action=print_version())

    # begin subparsers
    subparsers = parser.add_subparsers(
        metavar='command',
        dest='command',
        description='Each has its own [-h, --help] statement.')

    return parser
