from master.Project import Project

def do_list(args):
    p = Project.loadFromDisk('./')
    print('\n'.join(p.listTasks(args.filter)))
