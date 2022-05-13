from master.Project import Project


def do_list(args):
    p = Project.loadFromDisk(args.project)

    if args.filter:
        args.filter += ' and'
    if 'closed' not in args.filter:
        args.filter += ' t.stage != "closed"'
    else:
        args.filter += ' True'

    s = []
    for p, root, tasks in p.filteredTasks(args.filter, args.project):
        s.extend([f'{root}/{t.title}' for t in tasks])

    print('\n'.join(s).strip())
