import sys

from master.Project import Project
from master.util.edit import edit


def do_init(args):
    try:
        p = Project.initOnDisk(args.path, args.username, force=args.force)
    except FileExistsError as e:
        print('ERROR:', e, 'Run with "--force" to re-init.')
        sys.exit(1)
    except FileNotFoundError as e:
        print('ERROR: master cannot init in non-existent nested directories.')
        sys.exit(1)

    conffile = args.conf or f'{p.path}/project.yaml'

    with open(conffile) as f:
        s = f.read()

    try:
        edit(s, conffile)
    except ValueError as e:
        print('ERROR:', e)
        sys.exit(1)

    # This will verify the edits to the conf
    p = Project.loadFromDisk(args.path)
