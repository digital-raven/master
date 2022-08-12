def add_init_subparser(subparsers):

    init_parser = subparsers.add_parser(
        'init', help='Initialize a new project.',
        description='Initialize a new project.')

    init_parser.add_argument(
        'path', help='Directory to create project in.', default='.', nargs='?')

    init_parser.add_argument(
        '-c', '--conf', help=(
            'Specify a config template based on the purpose of this project.'
            'This may be a filename or one of the built-in templates agile, '
            'basic, calendar, or note. "basic" is the default.'),
        default='basic')

    init_parser.add_argument(
        '--force', help='Overwrite an existing project.', default=False, action='store_true')
