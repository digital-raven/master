import os
import sys

from libzet import load_zettels, move_zettels


def do_mv(args):

    # We can't move directories yet
    if any([os.path.isdir(t) for t in args.zettels]):
        print('ERROR: Cannot move directories.')
        sys.exit(1)

    zettels = load_zettels(args.zettels)
    move_zettels(zettels, args.dest)
