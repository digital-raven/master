from master.Project import Project

def do_add(args):
    args.project = args.project or './'
    p = Project.loadFromDisk(args.project)
    p.createTask(args.username, editor='vim')
