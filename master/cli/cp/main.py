from libzet import load_zettels, copy_zettels


def do_cp(args):

    zettels = load_zettels(args.zettels)
    copy_zettels(zettels, args.dest)
