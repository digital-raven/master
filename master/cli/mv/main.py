import os
import sys

from master.Project import Project
from master.Task import Task


def do_mv(args):
    """ mv is basically a copy followed by a removal.
    """

    # We can't move projects yet
    if any([os.path.isdir(t) for t in args.tasks]):
        print('ERROR: Cannot move entire projects.')
        sys.exit(1)

    dest = Project.loadFromDisk(args.dest, recursive=False)
    if dest is None:
        print(f'ERROR: "{args.dest}" is not host to a master project.')
        sys.exit(1)

    # Make sure dest isn't in the tasks being moved.
    for t in args.tasks:
        path = os.path.dirname(t) or './'
        if os.path.normpath(args.dest) == os.path.normpath(path):
            print('ERROR: Cannot move a task to its own project.')
            sys.exit(1)

    # Verify files exist and stuff before attempting moves
    projects = {}
    for task in args.tasks:
        path = os.path.dirname(task) or './'
        tid = os.path.basename(task).split('.rst')[0]

        if path not in projects:
            projects[path] = Project.loadFromDisk(path, recursive=False)

        if projects[path] is None:
            print(f'ERROR: "{path}" is not host to a master project.')
            sys.exit(1)

        try:
            task = projects[path].tasks[tid]
        except KeyError as e:
            tmp = os.path.normpath(f'./{path}/{tid}')
            print(f'ERROR: The task "{tmp}" does not exist.')
            sys.exit(1)

    failed_moves = []
    for task in args.tasks:
        path = os.path.dirname(task) or './'
        tid = os.path.basename(task).split('.rst')[0]

        try:
            task = projects[path].tasks[tid]
        except KeyError:
            failed_moves.append(task)

        dest.createTask(
            task.creator, task.title, task.description, task.attributes,
            creation_date=task.creation_date)

        projects[path].removeTask(tid)

    dest.flush()

    # Flush change to disk
    for project in projects.values():
        project.flush()

    if failed_moves:
        print('WARN: Failed to move the following tasks:')
        print('\n'.join(failed_moves))
