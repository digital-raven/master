""" Manage projects and tasks.
"""
import os
import re
from glob import glob

from libzet import Attributes, create_zettel, load_zettels
import yaml

from master.configs.note import note


class Project:

    def __init__(self, settings, tasks):
        """ Init a new Project.

        Projects have sub-projects, tasks, and settings loaded from a config.

        Any .rst files in the dir are assumed to be tasks. Any dirs are assumed
        to be subprojects. Each project has a general settings file that is
        always called "project.yaml".

        This is expected to be a singleton pattern; one and only one project
        instance should be loaded at any given root

        Args:
            name: Name of the project.
            tasks: List of tasks to add.

        Raises:
            ValueError if any of the tasks were invalid.
        """
        tasks = tasks or []

        self.tasks = tasks
        self.settings = Attributes(settings)

        if 'zettel_format' not in self.settings:
            self.settings['zettel_format'] = 'md'

    @classmethod
    def initOnDisk(cls, path, template='', force=False):
        """ Init a new project on the disk.

        A project is initialized by creating a ztemplate.yaml file in the
        directory.

        Args:
            path: Dir where to init the project.
            template: Yaml string or dir to be used as the template.
            force: Re-init over an existing ztemplate.yaml

        Returns:
            The newly initialized Project.

        Raises:
            FileExistsError: A project already exists at the specified path.
            PermissionError: User lacks permissions to create a new project.
            ValueError: Invalid template.
        """
        if os.path.exists(f'{path}/ztemplate.yaml') and not force:
            raise FileExistsError(f'Location {path} is already host to a project.')

        s = template if template else note
        if len(s.splitlines()) == 1:
            with open() as f:
                s = f.read()

        # Set the name of the project to the containing directory.
        if '__DEFAULT_PROJECT_NAME' in s:
            abspath = os.path.abspath(path)
            project_name = os.path.basename(abspath)
            s = s.replace('__DEFAULT_PROJECT_NAME', project_name)

        # Determine the task prefix
        # CAPS word if single word. Else abbreviation.
        if '__DEFAULT_PREFIX' in s:
            prefix = project_name.replace('-', '_').split('_')
            if len(prefix) == 1:
                prefix = ''.join(prefix[0]).upper()
            else:
                prefix = ''.join([x[0] for x in prefix]).upper()

            s = s.replace('__DEFAULT_PREFIX', f'{prefix}')

        # Make sure the template is valid yaml
        try:
            y = yaml.safe_load(s)
            if type(y) is str:
                raise ValueError('The template file was not valid yaml.')
        except yaml.scanner.ScannerError as e:
            raise ValueError(e)

        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        with open(f'{path}/ztemplate.yaml', 'w') as f:
            f.write(s)

        # Create the project by loading it back
        return Project.loadFromDisk(path)

    @classmethod
    def loadFromDisk(cls, path):
        """ Load a project from disk.

        Projects will be recursively loaded from a path on the
        filesystem. Each directory that contains a project.yaml
        file will be considered as a project.

        Args:
            path: Dir where project is located.

        Returns: A new Project instance. None if the path didn't
            contain a project config.
        """
        path = path or '.'
        try:
            settings = Attributes.fromYaml(f'{path}/ztemplate.yaml')
        except OSError:
            settings = {}

        p = Project(settings, None)

        # Init the project with current settings.
        fmt = p.settings['zettel_format']
        p.tasks = load_zettels(path, zettel_format=fmt)

        return p

    def createTask(self, path, title):
        """ Create a new task for this project.

        The task will also be written to disk.

        Args:
            creator: Username of the person creating the task.
            title: Optional title of the new task.

        Returns:
            A reference to the newly created task.

        Raises:
            ValueError if the task was invalid.
        """
        fmt = self.settings['zettel_format']
        title = title or 'MyNewZettel'
        if 'task_prefix' in self.settings:
            newid = 1
            prefix = self.settings['task_prefix']
            while os.path.exists(f'{path}/{prefix}-{newid}.{fmt}'):
                newid += 1

            title = f'{prefix}-{newid}'

        path = f'{path}/{title}.{fmt}'

        z = create_zettel(path, title=f'{title}', zettel_format=fmt)

        self.tasks.append(z)
        return z
