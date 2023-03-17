def add_list_subparser(subparsers):

    parser = subparsers.add_parser(
        'list', help='List the title of tasks according to a filter.',
        description='List the title of tasks according to a filter.')

    parser.add_argument(
        '-f', '--filter', help='Specify a list filter.', default='True')

    parser.add_argument(
        'zettels', help='Files and directories to filter.', default='.', nargs='*')
