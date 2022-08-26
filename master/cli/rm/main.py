import os
import sys

from master.Project import Project


def do_rm(args):

    # Don't remove directories
    if any([os.path.isdir(t) for t in args.tasks]):
        print('ERROR: Cannot remove directories.')
        sys.exit(1)

    # Remove tasks but don't commit yet
    projects = {}
    failed_removals = []
    for task in args.tasks:
        path = os.path.dirname(task) or './'
        tid = os.path.basename(task).split('.rst')[0]

        if path not in projects:
            projects[path] = Project.loadFromDisk(path, recursive=False)

        if projects[path] is None:
            print(f'ERROR: "{path}" is not host to a master project.')
            sys.exit(1)

        try:
            projects[path].removeTask(tid)
        except KeyError:
            failed_removals.append(task)

    # Flush change to disk
    for project in projects.values():
        project.flush()

    if failed_removals:
        print('WARN: Failed to remove the following tasks:')
        print('\n'.join(failed_removals))
