def add_init_subparser(subparsers):

    init_parser = subparsers.add_parser(
        'init', help='Initialize a new project.',
        description='Initialize a new project.')

    init_parser.add_argument(
        'path', help='Directory to create project in.', default='.', nargs='?')

    init_parser.add_argument(
        '--conf', help='Specify a custom config.', default='')

    init_parser.add_argument(
        '--force', help='Overwrite an existing project.', default=False, action='store_true')
