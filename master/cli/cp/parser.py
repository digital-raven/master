def add_cp_subparser(subparsers):

    parser = subparsers.add_parser(
        'cp', help='Copy a task to a new project.',
        description='Any incorrect metadata will be corrected.')

    parser.add_argument(
        'tasks', metavar='task', help='Tasks to remove.', nargs='+')

    parser.add_argument('dest', help='Destination project.')
