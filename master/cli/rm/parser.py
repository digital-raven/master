def add_rm_subparser(subparsers):

    parser = subparsers.add_parser(
        'rm', help='Remove tasks from their projects.',
        description='Remove tasks from their projects.')

    parser.add_argument(
        'tasks', metavar='task', help='Tasks to remove.', nargs='+')
