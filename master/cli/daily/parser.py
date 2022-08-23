from daily.parser import create_add_subparser, create_show_subparser


def add_daily_subparser(subparsers):
    parser = subparsers.add_parser(
        'daily', help="Master's daily entry command.",
        description='Leverages the daily program for daily entries.')

    # begin subparsers
    subparsers = parser.add_subparsers(
        metavar='command', dest='daily_subcommand', required=True,
        description='Each has its own [-h, --help] statement.')

    # Add supported sub-commands
    sp = create_add_subparser(subparsers)
    sp = create_show_subparser(subparsers)

    sp.add_argument(
        '-u', '--username', help="Show a specific user's journal")
