"""
A simple example of testing the solution to assignment1.py.
From this directory, you can run:
  pygrade grade -s students.tsv -t test_assignment1.py

This will generate grades.json.

The file name is relative to each student's github repo:
@name=example/assignment1.py
Here we list the total possible points for the assignment:
@possible_points=5
"""
import unittest
from assignment1 import *


class TestAssignment1(unittest.TestCase):
    def test_simple_1(self):
        """
        We specify the point value for each test in the method comment string:
        @points=2
        """
        self.assertTrue(is_mammal('cat'))

    def test_simple_2(self):
        """ @points=2 """
        self.assertTrue(is_mammal('dog'))

    def test_hard(self):
        """ @points=1 """
        self.assertTrue(is_mammal('dolphin'))
