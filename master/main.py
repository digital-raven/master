""" main entry point for master.
"""

import importlib
import os
import sys

import argcomplete

from master.parser import create_parser
from master.config import add_config_args, do_first_time_setup, user_conf


def main():
    parser = create_parser()
    argcomplete.autocomplete(parser)

    # Default daily command should be add
    if sys.argv[-1] == 'daily':
        sys.argv.append('add')

    args = parser.parse_args()

    if not os.path.exists(user_conf) or args.setup:
        print(f'INFO: Performing first-use setup.')
        do_first_time_setup()
        print(f'Setup complete. User config initialized at {user_conf}')
        print('Run "master -h" to see usage help.')
        sys.exit(0)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # fill in args with values from config.
    args = add_config_args(args, user_conf)

    if not args.username or not args.email:
        print(f'Username and/or email missing in {user_conf}')
        sys.exit(1)

    subcommand = importlib.import_module('master.cli.{}.main'.format(args.command))
    subcommand = getattr(subcommand, 'do_{}'.format(args.command))

    try:
        subcommand(args)
    except KeyboardInterrupt:
        print('Interrupt caught - closing.')

    sys.exit(0)


if __name__ == '__main__':
    main()
