import os
import shutil
import unittest

from master.Project import Project


resources = '{}/resources'.format(os.path.dirname(__file__))


class TestProject(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(f'{resources}/test_project'):
            shutil.rmtree(f'{resources}/test_project')

    def test_project_creation(self):
        """ Test initial project creation

        The name should be the basename of the path, the path should just
        be the path, it should have no tasks or sub-projects, and it should
        have barebones settings.
        """
        exp_name = 'test_project'
        p = Project.initOnDisk(f'{resources}/{exp_name}', 'tester')

        self.assertEqual(exp_name, p.name)
        self.assertEqual(f'{resources}/{exp_name}', p.path)

        self.assertEqual(dict(), p.projects)
        self.assertEqual(dict(), p.tasks)

        exp_attr = {'creation_date', 'creator', 'id', 'project', 'stage', 'tags'}

        self.assertEqual('tester', p.settings['owners'])
        self.assertEqual(exp_attr, p.settings['default_attributes'])
        self.assertEqual({'stage': 'todo'}, p.settings['default_attribute_values'])
        self.assertEqual(exp_name, p.settings['project_name'])
        self.assertEqual('TP_', p.settings['task_prefix'])

    def test_loading_from_disk(self):
        """ A project should be loadable from disk.
        """
        exp = Project.initOnDisk(f'{resources}/test_project', 'tester')
        p2 = Project.loadFromDisk(f'{resources}/test_project')

        self.assertEqual(exp.__dict__, p2.__dict__)

    def test_task_creation(self):
        """ Basic task creation by a project.

        New tasks should have the correct prefix and project name.
        """
        path = f'{resources}/test_project'
        p = Project.initOnDisk(path, 'tester')
        t = p.createTask('spongebob', 'My title', 'description')

        self.assertTrue(os.path.exists(f'{path}/{t.id}.rst'))
        self.assertTrue(p.tasks[t.id] is t)
        self.assertEqual('TP_1', t.id)
        self.assertEqual('spongebob', t.creator)
        self.assertEqual('TP_1: My title', t.title)
        self.assertEqual('description', t.description)
        self.assertEqual('test_project', t.project)

    def test_project_creation_with_conf(self):
        """ Projects created with a custom conf should have those settings.

        Also that dates aren't processed if they're empty strings.
        """
        path = f'{resources}/test_project'
        p = Project.initOnDisk(path, 'tester', f'{resources}/custom.conf')
        self.assertTrue('due_date' in p.settings['default_attributes'])
        self.assertTrue('testattr' in p.settings['default_attribute_values'])

        t = p.createTask('spongebob', 'My title', 'description')

        self.assertEqual('', t.due_date)
        self.assertEqual('Im a value', t.testattr)

    def test_project_creation_with_conf_not_exist(self):
        """ Not existent conf file should raise FileNotfoundError
        """
        with self.assertRaises(FileNotFoundError):
            p = Project.initOnDisk(f'{resources}/test_project', 'tester', 'not-exist')

    def test_project_creation_existing_dir(self):
        """ There should be no error for an existing directory.
        """
        os.mkdir(f'{resources}/test_project')
        p = Project.initOnDisk(f'{resources}/test_project', 'tester')
        self.assertTrue(os.path.exists(f'{resources}/test_project/.master.project'))

    def test_project_creation_at_existing_project(self):
        """ It should fail to init a project in an existing project.
        """
        p = Project.initOnDisk(f'{resources}/test_project', 'tester')
        with self.assertRaises(FileExistsError):
            p = Project.initOnDisk(f'{resources}/test_project', 'tester')

    def test_project_creation_failure_nested_dirs(self):
        """ It should fail to init a project in non-existent dirs.
        """
        with self.assertRaises(FileNotFoundError):
            p = Project.initOnDisk(f'{resources}/not-exist/test_project', 'tester')

    def test_sub_project_loading(self):
        """ Projects should load sub-projects
        """
        Project.initOnDisk(f'{resources}/test_project', 'tester')
        Project.initOnDisk(f'{resources}/test_project/sub_project', 'tester')

        p = Project.loadFromDisk(f'{resources}/test_project')

        # Should be accessible via dot-operator.
        sp = p.sub_project

        self.assertIs(p.projects['sub_project'], sp)

        self.assertEqual('test_project', p.name)
        self.assertEqual('sub_project', sp.name)

    def test_sub_project_addition(self):
        """ Projects should add sub-projects.

        Project addition should create the project if it doesn't exist.
        """
        p = Project.initOnDisk(f'{resources}/test_project', 'tester')
        sp1 = p.addProject('sub_project', 'tester')

        sp2 = Project.loadFromDisk(f'{resources}/test_project/sub_project')

        self.assertIs(p.sub_project, sp1)
        self.assertEqual(sp1.__dict__, sp2.__dict__)


if __name__ == '__main__':
    unittest.main()
