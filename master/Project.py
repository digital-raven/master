""" Manage projects and tasks.
"""
import os
import re
import sys
import tempfile
from subprocess import call

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


def editTask(task, editor):
    """ Open task in editor with a tmp file.

    This function does not return a task; it returns the task's RST. Check
    the validity of this output like this...

        # ... init some Task t
        # ...
        try:
            rst = editTask(t, 'vim')
            t = Task.createFromRst(rst)
        except ValueError:
            # handle the exception.

    Returns:
        The text from the tmp file.
    """
    _, path = tempfile.mkstemp(suffix='.rst')

    try:
        with open(path, 'w') as f:
            f.write(task.getRst())

        call([editor, path])

        with open(path, 'r') as f:
            text = f.read()

    finally:
        os.remove(path)

    return text


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
            tasks: List of tasks to add.
            settings: Dict of config settings loaded from project's conf.

        Raises:
            ValueError if any of the tasks were invalid.
        """
        self.name = name
        self.path = os.path.abspath(path)
        self.projects = projects
        self.tasks = {}
        self.settings = settings

        # List of modified tasks.
        self.modified = {}
        self.max_id = 0

        # Load the default attributes
        if 'default_attributes' in self.settings:
            tmp = {x.strip() for x in self.settings['default_attributes'].splitlines() if x.strip()}
            self.settings['default_attributes'] = tmp
        else:
            self.settings['default_attributes'] = set()

        # Load the default_attribute_values
        if 'default_attribute_values' in self.settings:
            tmp = {}
            lines = self.settings['default_attribute_values'].splitlines()
            for df in lines:
                df = df.split(':')
                tmp[df[0].strip()] = ':'.join(df[1:]).strip()
            self.settings['default_attribute_values'] = tmp
        else:
            self.settings['default_attribute_values'] = dict()

        self.check()

        # Add the tasks to this project
        for task in tasks:
            self.addTask(task, task.id)

    def check(self):
        """ Ensure all settings are valid python3 identifiers.

        Raises:
            ValueError if a project setting was invalid.
        """
        invalids = []
        for k in self.settings:
            if not k.isidentifier():
                invalids.append(k)

        for k in self.settings['default_attributes']:
            if not k.isidentifier():
                invalids.append(k)

        for k in self.settings['default_attribute_values']:
            if not k.isidentifier():
                invalids.append(k)

        if invalids:
            invalids = ', '.join(invalids)
            s = 'The following project settings are invalid identifiers'
            raise ValueError(f'{s}: {invalids}')

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
    def loadFromDisk(cls, path, pattern=''):
        """ Load a project from disk.

        Projects will be recursively loaded from a path on the
        filesystem. Each directory that contains a .master.project
        file will be considered as a project.

        Args:
            path: Dir where projects are located.
            pattern: Load files that match the pattern. Will default
                to '^{task_prefix}.+\.rst$' if not provided.

        Returns: A new Project instance. None if the path didn't
            contain a project config.
        """
        r, d, f = readdir_(path)

        try:
            settings = colonconf.load(f'{r}/.master.project')
        except (FileNotFoundError, PermissionError):
            return None

        # Init the project with current settings.
        project = Project(settings['project_name'], r, {}, {}, settings)

        if not pattern:
            prefix = project.settings['task_prefix']
            pattern = f'^{prefix}[0-9]+\.rst$'

        # Load tasks.
        invalid_tasks = ''
        taskfiles = [f'{r}/{x}' for x in f if re.search(pattern, x)]
        try:
            project.loadTasks(taskfiles)
        except ValueError as ve:
            invalid_tasks = f'The project {r} has invalid tasks.\n' + str(ve) + '\n'

        # Load projects.
        projects = {}
        invalid_projects = []
        for proj in [f'{r}/{x}' for x in d]:
            try:
                p = Project.loadFromDisk(proj)
                if p:
                    projects[p.name] = p
            except ValueError as ve:
                invalid_projects.append(str(ve))

        if invalid_tasks or invalid_projects:
            raise ValueError('\n'.join(invalid_tasks + invalid_projects))

        project.projects = projects

        return project

    def loadTasks(self, tasks):
        """ Load tasks into this project from disk.

        Args:
            tasks: A list of files to load from.

        Raises:
            ValueError if any of the tasks were invalid. Valid
            tasks will still be loaded.
        """
        errors = []
        new_tasks = []
        for task in tasks:
            try:
                self.loadTask(task)
            except ValueError as ve:
                errors.append(f'{t}: {ve}')

        if errors:
            raise ValueError('\n'.join(errors))

    def loadTask(self, task):
        """ Load a task from a file.

        The task will be corrected as it's read in.

        Args:
            task: Filepath to load task from.

        Raises:
            ValueError if the task was invalid.
        """
        exp_id = os.path.basename(task).split('.')[0]
        try:
            t = Task.createFromRst(task)
            self.addTask(t, exp_id)
        except ValueError as ve:
            raise ValueError(f'{rst}: {ve}')

    def addTask(self, task, exp_id=''):
        """ Add a new task to this project.

        The task will be corrected.

        Args:
            task: Task reference to add.
            exp_id: Expected ID for the task to have.

        Raises:
            ValueError if the task was invalid and could not
            be corrected.
        """
        corrected = self._correctTask(task, exp_id)
        if corrected:
            self.modified[task.id] = task

        self._addTask(task)

    def _addTask(self, task):
        """ Blindly adds a task without correction

        Only send corrected tasks to this method.
        """
        self.tasks[task.id] = task

        # Update max_id
        cur_id = int(task.id.split('_')[-1])
        self.max_id = max(self.max_id, cur_id)

    def _correctTask(self, t, exp_id, creation_date='', creator=''):
        """ Correct a task's metadata.

        Args:
            t: Task to be corrected.
            exp_id: Expected ID of the task.
            creation_date: Expected original creation date.
            creator: Expected creator of the task.

        Returns:
            True if the task required a correction. False otherwise.

        Raise:
            ValueError if the task was invalid and therefore uncorrectable.
        """
        corrected = False

        # Default the creation_date to 'today'
        if 'creation_date' not in t.attributes:
            t.attributes['creation_date'] = 'today'
            corrected = True

        # Ensure the creation_date isn't modified.
        if creation_date and t.creation_date != creation_date:
            t.creation_date = creation_date
            corrected = True

        # Ensure each task has a creator field.
        if 'creator' not in t.attributes or (creator and creator != t.creator):
            t.attributes['creator'] = creator
            corrected = True

        # Correct the ID.
        if 'id' not in t.attributes or (exp_id and t.id != exp_id):
            t.attributes['id'] = exp_id
            corrected = True

        # Check the ID
        if not re.search('_[0-9]+$', t.id):
            raise ValueError(f'Invalid ID {t.id}')

        # The task always belongs to this project.
        if 'project' not in t.attributes or t.project != self.name:
            t.attributes['project'] = self.name
            corrected = True

        # All tasks require a stage
        if 'stage' not in t.attributes:
            t.attributes['stage'] = 'todo'
            corrected = True

        # All tasks must have tags as a list.
        if 'tags' not in t.attributes or type(t.tags) is not list:
            t.attributes['tags'] = []
            corrected = True

        # The ID should prefix the title
        if not t.title.startswith(t.id):
            t.title = f'{t.id}: {t.title}'
            corrected = True

        # Ensure the task has all expected default attributes.
        for k in self.settings['default_attributes']:
            if k not in t.attributes:
                t.attributes[k] = ''
                corrected = True

        t.check()
        t.refresh()

        return corrected

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

        Raises:
            ValueError if the task was invalid.
        """
        attrs = attrs or {}

        # Set default_attribute_values
        attrs.update(self.settings['default_attribute_values'])

        attrs['creator'] = creator
        attrs['creation_date'] = 'today'
        attrs['id'] = self.settings['task_prefix'] + str(self.max_id + 1)

        task = Task(title, description, attrs)
        self.addTask(task)

        self.updateTask(task, editor)
        return task

    def updateTask(self, task, editor=''):
        """ Add a task to this project or modify an existing one.

        If the new task has a conflicting ID with an existing task, then the
        existing task will be overwritten.

        Args:
            task: Task to update.
            editor: Path to editor to edit the task.

        Returns:
            A reference to the updated task.
        """

        # A task's ID and creator should not be modifiable.
        orig_id = task.id
        orig_creation_date = task.creation_date
        orig_creator = task.creator

        # Correct the task before and after editing.
        self._correctTask(task, orig_id)

        if editor:
            text = editTask(task, editor)
            try:
                task = Task.createFromRst(text)
            except ValueError as ve:
                with open(f'task.bkp.rst', 'w') as f:
                    f.write(text.strip() + '\n')
                raise ValueError(
                    f'The created task was invalid. Your text has been '
                    f'saved to task.bkp.rst.\n'
                    f'Reason: {ve}')

        self._correctTask(task, orig_id, orig_creation_date, orig_creator)

        self.tasks[task.id] = task
        self.modified[task.id] = task

        cur_id = int(task.id.split('_')[-1])
        self.max_id = max(self.max_id, cur_id)

        self.dump()

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
