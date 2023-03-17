def add_edit_subparser(subparsers):

    parser = subparsers.add_parser(
        'edit', help='Edit existing zettels.',
        description='Edit existing zettels.')

    parser.add_argument(
        'zettels', metavar='zettel', help='Zettels to edit.', nargs='+')

    parser.add_argument('--headings', help='Edit select headings.', nargs='+')
