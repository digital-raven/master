import os

from master.Project import Project


def do_add(args):
    args.project = args.project or './'
    p = Project.loadFromDisk(args.project)

    title = ''
    if not os.path.isdir(args.project):
        title = os.path.basename(args.project)
        args.project = os.path.dirname(args.project)

    p.createTask(args.project, title)
