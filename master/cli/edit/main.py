from libzet import load_zettels, edit_zettels


def do_edit(args):

    zettels = load_zettels(args.zettels)
    edit_zettels(zettels, headings=args.headings, delete=True)
