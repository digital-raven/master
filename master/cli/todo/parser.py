def add_todo_subparser(subparsers):

    parser = subparsers.add_parser(
        'todo', help='Print what you should do today.',
        description='Print what you should do today.')

    parser.add_argument(
        'zettels', metavar='zettel', default='.', nargs='*',
        help='Paths (dirs or files) to zettels.')

    parser.add_argument(
        '-d', '--date', help='Print what should be done for a given date.',
        default='today')

    parser.add_argument(
        '--list-active', help='Print events that have yet to occur or expire.',
        action='store_true')

    parser.add_argument(
        '--remind', help='Use this flag to pipe output to remind.',
        action='store_true')
