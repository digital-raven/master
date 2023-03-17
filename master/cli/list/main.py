from libzet import load_zettels


def _filter_zettels(zettels, filter):
    return [z for z in zettels if eval(filter)]


def do_list(args):

    zettels = load_zettels(args.zettels)

    filtered = _filter_zettels(zettels, args.filter)
    filtered = sorted([f'{z.attrs["_loadpath"]}: {z.title}' for z in filtered])
    print('\n'.join(filtered))
