def add_add_subparser(subparsers):

    parser = subparsers.add_parser(
        'add', help='Add a task to a project.',
        description='Add a task to a project.')

    parser.add_argument(
        'project', help='Path to project to add the task.', default='./', nargs='?')
