def add_rm_subparser(subparsers):

    parser = subparsers.add_parser(
        'rm', help='Remove zettels.',
        description='Remove zettels.')

    parser.add_argument(
        'zettels', metavar='zettel', help='Zettels to remove.', nargs='+')
