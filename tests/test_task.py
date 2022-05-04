import os
import unittest
from datetime import datetime

from master.Task import Task
from master.Task import parse_date


resources = '{}/resources'.format(os.path.dirname(__file__))


class TestTask(unittest.TestCase):

    def test_rst_creation(self):
        """ Tasks can be created from RST text.
        """
        t = Task.createFromRst(f'{resources}/basic.rst')
        with open(f'{resources}/basic.rst') as f:
            exp = f.read()

        self.assertEqual(exp, t.getRst())

    def test_alphabetized_attributes(self):
        """ Tasks should alphabetize attributes when printing.
        """
        t = Task.createFromRst(f'{resources}/out-of-order.rst')
        with open(f'{resources}/in-order.rst') as f:
            exp = f.read()
        self.assertEqual(exp, t.getRst())

    def test_humanized_date(self):
        """ Values that contain "date" should be parsed.
        """
        t = Task.createFromRst(f'{resources}/human-date.rst')
        exp_date = parse_date('today')
        exp_duedate = parse_date('next wednesday')

        self.assertEqual(exp_date, t.creation_date)
        self.assertEqual(exp_duedate, t.due_date)

    def test_trailing_space(self):
        """ Task parsing should trim trailing spaces.
        """
        t = Task.createFromRst(f'{resources}/trailing-lines.rst')
        with open(f'{resources}/basic.rst') as f:
            exp = f.read().strip() + '\n'

        self.assertEqual(exp, t.getRst())


if __name__ == '__main__':
    unittest.main()
