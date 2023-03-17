import os
import sys

from libzet import load_zettels, delete_zettels


def do_rm(args):

    # Don't remove directories
    if any([os.path.isdir(t) for t in args.zettels]):
        print('ERROR: Cannot remove directories.')
        sys.exit(1)

    zettels = load_zettels(args.zettels)
    delete_zettels(zettels)
