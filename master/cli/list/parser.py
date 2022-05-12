def add_list_subparser(subparsers):

    parser = subparsers.add_parser(
        'list', help='List the title of tasks according to a filter.',
        description='List the title of tasks according to a filter.')

    parser.add_argument(
        'filter', help='Specify a list filter.', default='', nargs='?')
