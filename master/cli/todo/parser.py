def add_todo_subparser(subparsers):

    parser = subparsers.add_parser(
        'todo', help='Print what you should do today.',
        description='Print what you should do today.')

    parser.add_argument(
        'project', help='Only account for tasks at or below this project.',
        default='.', nargs='?')

    parser.add_argument(
        '-d', '--date', help='Print what should be done for a given date.',
        default='today')

    parser.add_argument(
        '--list-active', help='Print events that have yet to occur or expire.',
        action='store_true')

    parser.add_argument(
        '--remind', help='Use this flag to pipe output to remind.',
        action='store_true')
