def add_mv_subparser(subparsers):

    parser = subparsers.add_parser(
        'mv', help='Move zettels.',
        description='Move zettels.')

    parser.add_argument(
        'zettels', metavar='zettel', help='Zettels to move.', nargs='+')

    parser.add_argument('dest', help='Destination.')
