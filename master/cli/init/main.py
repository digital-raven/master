from master.Project import Project
from master.util.edit import edit


def do_init(args):
    p = Project.initOnDisk(args.path, args.username)
    conffile = args.conf or f'{p.path}/project.yaml'

    with open(conffile) as f:
        s = f.read()

    edit(s, conffile)

    # This will verify the edits to the conf
    p = Project.loadFromDisk(args.path)
