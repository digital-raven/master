def add_mv_subparser(subparsers):

    parser = subparsers.add_parser(
        'mv', help='Move tasks to a new project.',
        description='Any incorrect metadata will be corrected.')

    parser.add_argument(
        'tasks', metavar='task', help='Tasks to remove.', nargs='+')

    parser.add_argument('dest', help='Destination project.')
