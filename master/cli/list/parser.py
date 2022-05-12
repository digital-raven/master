def add_list_subparser(subparsers):

    parser = subparsers.add_parser(
        'list', help='List the title of tasks according to a filter.',
        description='List the title of tasks according to a filter.')

    parser.add_argument(
        '-f', '--filter', help='Specify a list filter.', default='')

    parser.add_argument(
        'project', help='Target a specific project.', default='.', nargs='?')
