from master.Project import Project


def do_list(args):
    p = Project.loadFromDisk(args.project)

    for p, root, tasks in p.filteredTasks(args.filter, args.project):
        print('\n'.join([f'{root}/{t.title}' for t in tasks]))
