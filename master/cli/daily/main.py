import importlib
import os
import sys

from master.Project import readdir_


def find_root(start):
    """ Walk up from start to find root of the project tree.

    Args:
        start: Starting path.

    Returns:
        Path to root of the project tree.

    Raises:
        ValueError: start is not a part of a project tree.
    """
    cwd = None
    r, _, f = readdir_(start)
    while 'project.yaml' in f:
        cwd = r
        start += '/../'
        r, _, f = readdir_(start)

    return cwd


def do_daily(args):
    root = find_root('./')
    if not root:
        print('ERROR: This dir is not a master project.')
        sys.exit(1)

    os.makedirs(f'{root}/users/{args.username}', exist_ok=True)

    args.journal = f'{root}/users/{args.username}/journal.json'

    subcommand = importlib.import_module(f'daily.cli.{args.daily_subcommand}')
    subcommand = getattr(subcommand, f'do_{args.daily_subcommand}')

    subcommand(args)

    sys.exit(0)
