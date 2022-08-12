from master.Project import Project


def do_edit(args):
    if not args.task.startswith('./'):
        args.task = './' + args.task

    proj_path = '/'.join(args.task.split('/')[:-1])
    p = Project.loadFromDisk(proj_path)

    if args.task.endswith('.rst'):
        args.task = args.task[:-4]

    if '/' in args.task:
        args.task = args.task.split('/')[-1]

    task = eval(f'p.{args.task}')
    p.updateTask(task, editor='vim')
    p.flush()
