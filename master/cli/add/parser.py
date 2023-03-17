def add_add_subparser(subparsers):

    parser = subparsers.add_parser(
        'add', help='Add a zettel to a project.',
        description='Add a zettel to a project.')

    parser.add_argument(
        'project', help='Path to add the zettel.', default='./', nargs='?')
