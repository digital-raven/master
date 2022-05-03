""" Manage projects and tasks.
"""
import os
import sys

from master import colonconf
from master.Task import Task


def readdir_(d):
    """ Same as os.walk executed at the first level.

    Returns:
        A 3-tuple. First entry is the root (d), second is a list of all
        directory entries within d, and the third is a list of names of
        regular files.
    """
    d = d.rstrip(os.path.sep)
    if not os.path.isdir(d):
        raise ValueError('"{}" is not a directory.'.format(d))

    for root, dirs, files in os.walk(d):
        return root, dirs, files


class Project:

    def __init__(self, name, path, projects, tasks, settings):
        """ Init a new Project.

        Projects have sub-projects, tasks, and settings loaded from a config.

        Any .rst files in the dir are assumed to be tasks. Any dirs are assumed
        to be subprojects. Each project has a general settings file that is
        always called ".master.project".

        This is expected to be a singleton pattern; one and only one project
        instance should be loaded at any given root

        Args:
            name: Name of the project.
            path: Path of the project on disk.
            projects: Dictionary of other projects under this one.
            tasks: Dictionary of Tasks. Key should be the ID of the task.
            settings: Dict of config settings loaded from project's conf.
        """
        self.name = name
        self.path = os.path.abspath(path)
        self.projects = projects
        self.tasks = {}
        self.settings = settings

        # List of modified tasks.
        self.modified = {}
        self.max_id = 1
        for task in tasks.values():
            self.addTask(task)

        # Reset self.modified since the project hasn't changed anything on disk.
        self.modified = {}

    @classmethod
    def initOnDisk(cls, path, creator, conf=''):
        """ Init a new project on the disk.

        A project is initialized by creating a .master.project file in the
        directory. No sub-projects or tasks will be created. Pre-existing
        files will not be modified, but this function is designed to be called
        on a non-existent or empty directory.

        The default, barebones settings that will be created by default are...

            owners = creator
            default_attributes = ''
            default_attribute_values  = ''
            project_name = <basename of path>
            task_prefix = <ALL CAPS of project_name> or..
                <ALL CAPS OF FIRST LETTER OF EACH WORD IN PROJECT NAME> if
                project has multiple words in its name.

        Args:
            path: Dir where to init the project.
            creator: Username of the project's creator. Will have absolute
                authority over this and any projects owned by this project.
            conf: Path to configuration outlining default settings.

        Returns:
            The newly initialized Project.

        Raises:
            FileExistsError: A project already exists at the specified path.
            PermissionError: User lacks permissions to create a new project.
        """
        path = os.path.abspath(path)
        if os.path.exists(f'{path}/.master.project'):
            raise FileExistsError(f'Location {path} is already host to a project.')

        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        settings = {
            'default_attributes': '',
            'default_attribute_values': '',
        }

        if conf:
            settings.update(colonconf.load(f'{conf}'))

        # Default the owner of the project to its creator.
        settings['owners'] = creator

        # Set the name of the project to the containing directory.
        settings['project_name'] = os.path.basename(path)

        # Determine the task prefix
        prefix = settings['project_name'].split('_')
        if len(prefix) == 1:
            prefix = ''.join(prefix[0]).upper()
        else:
            prefix = ''.join([x[0] for x in prefix]).upper()

        settings['task_prefix'] = f'{prefix}_'

        # Write the configuration to file
        colonconf.dump(f'{path}/.master.project', settings)

        # Create the project by loading it back
        return Project.loadFromDisk(path)

    @classmethod
    def loadFromDisk(cls, path):
        """ Load a project from disk.

        Projects will be recursively loaded from a path on the
        filesystem. Each directory that contains a .master.project
        file will be considered as a project.

        Args:
            path: Dir where projects are located.

        Returns: A new Project instance. None if the path didn't
            contain a project config.
        """
        r, d, f = readdir_(path)

        try:
            settings = colonconf.load(f'{r}/.master.project')
        except (FileNotFoundError, PermissionError):
            return None

        projects = {f'{x}': Project.loadFromDisk(f'{r}/{x}') for x in d}
        projects = {k: v for k, v in projects.items() if v}
        tasks = {x: Task.createFromRst(x) for x in f if x.endswith('.rst')}

        return Project(settings['project_name'], r, projects, tasks, settings)

    def createTask(self, creator, title='', description='', attrs=None, editor=''):
        """ Create a new task for this project.

        The task will also be written to disk.

        Args:
            creator: Username of the person creating the task.
            editor: Open the task for editing in the specified editor.
            title: Optional title of the new task.
            description: Optional description of the new task.
            attrs: Additional desired attrs of the task. creator,
                creation_date, id, and the project name cannot be overridden.

        Returns:
            A reference to the newly created task.
        """
        attrs = attrs or {}
        if 'default_attributes' in self.settings:
            attrs = {k: '' for k in self.settings['default_attributes'].splitlines()}

        # Override other default behavior with default_attribute_values
        if 'default_attribute_values' in self.settings:
            default_values = self.settings['default_attribute_values'].splitlines()
            for df in default_values:
                df = df.split(':')
                k, v = df[0].strip(), ':'.join(df[1:]).strip()
                attrs[k] = v

        attrs['creator'] = creator
        attrs['creation_date'] = 'today'
        attrs['id'] = self.settings['task_prefix'] + str(self.max_id)
        attrs['project'] = self.name

        task = Task(title, description, attrs)

        # TODO: Open task in editor
        #

        self.addTask(task)
        self.dump()
        return task

    def addTask(self, task):
        """ Add a task to this project or modify an existing one.

        The new task will be queued for dumping. If this isn't desired
        then set self.modified to {} after calling.

        If the new task has a conflicting ID with an existing task, then the
        existing task will be overwritten.

        Args:
            task: New task to add.
        """
        self.tasks[task.id] = task
        self.modified[task.id] = task

        cur_id = int(task.id.split('_')[-1])
        self.max_id = max(self.max_id, cur_id)
        self.max_id += 1

    def addProject(self, name, creator, conf=''):
        """ Add a new project under this project.

        The project will be created on disk if it doesn't exist.

        Args:
            name: Name of the project.
            creator: Person who created it.
            conf: Optional beginning project configuration.

        Returns:
            A reference to the newly added project.
        """
        try:
            p = Project.loadFromDisk(f'{self.path}/{name}')
        except ValueError:
            p = None

        if not p:
            p = Project.initOnDisk(f'{self.path}/{name}', creator, conf)

        self.projects[name] = p
        return p

    def dump(self):
        """ Write changes to this project back to disk.
        """
        for id_, task in self.modified.items():
            with open(f'{self.path}/{id_}.rst', 'w') as f:
                f.write(task.getRst())

        self.modified = {}

    def __getattr__(self, key):
        """ Expose keys in values as attributes.
        """
        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self.projects:
            return self.projects[key]
        elif key in self.tasks:
            return self.tasks[key]

        raise AttributeError(f"'Project' object has no attribute {key}")
