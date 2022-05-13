def add_todo_subparser(subparsers):

    parser = subparsers.add_parser(
        'todo', help='Print what you should do today.',
        description='Print what you should do today.')

    parser.add_argument(
        'project', help='Only account for tasks at or below this project.',
        default='.', nargs='?')
