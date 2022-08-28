import os
import sys

from master.Project import Project
from master.Task import Task


def do_cp(args):

    # We can't copy projects... yet
    if any([os.path.isdir(t) for t in args.tasks]):
        print('ERROR: Cannot copy entire projects.')
        sys.exit(1)

    project = Project.loadFromDisk(args.dest, recursive=False)
    if project is None:
        print(f'ERROR: "{args.dest}" is not host to a master project.')
        sys.exit(1)

    # Load tasks into memory
    try:
        tasks = [Task.createFromRst(t) for t in args.tasks]
    except (FileNotFoundError, PermissionError) as e:
        print(f'ERROR: {e}')
        sys.exit(1)

    # Copy and write tasks to disk
    for t in tasks:
        t.attributes['creation_date'] = 'now'
        project.createTask(args.username, t.title, t.description, t.attributes)

    project.flush()
