def add_cp_subparser(subparsers):

    parser = subparsers.add_parser(
        'cp', help='Copy zettels.',
        description='Copy zettels.')

    parser.add_argument(
        'zettels', metavar='task', help='Zettels to copy.', nargs='+')

    parser.add_argument('dest', help='Destination.')
