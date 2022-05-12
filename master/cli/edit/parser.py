def add_edit_subparser(subparsers):

    parser = subparsers.add_parser(
        'edit', help='Edit an existing task.',
        description='Edit an existing task.')

    parser.add_argument(
        'task', help='Name or path of task.')
