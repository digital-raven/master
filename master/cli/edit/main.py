from master.Project import Project

def do_edit(args):
    p = Project.loadFromDisk('./')

    if args.task.endswith('.rst'):
        args.task = args.task[:-4]

    if args.task.startswith('./'):
        args.task = args.task[2:]

    args.task = ''.join(args.task.replace('/', '.'))

    task = eval(f'p.{args.task}')
    p.updateTask(task, editor='vim')
