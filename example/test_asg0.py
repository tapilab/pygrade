"""
A simple example of testing the solution to:
https://github.com/tapilab/pygrade-example-assignment/blob/master/asg0/asg0.py

We use special strings @name and @possible_points to identify the file(s) and point
total for this assignment. Multiple files can be listed, separated by commas.

@name=asg0/asg0.py
@possible_points=20
"""
import unittest
from asg0 import *


class TestAssignment1(unittest.TestCase):
    """
    Here, we write unit tests for the assignment.
    Each test has a special string @points that specifies
    the amount to be deducted upon failure.
    Note that the @points add up to @possible_points (20).
    """
    def test_simple_1(self):
        """
        We specify the point value for each test in the method comment string:
        @points=4
        """
        self.assertTrue(is_mammal('cat'))

    def test_simple_2(self):
        """ @points=4 """
        self.assertTrue(is_mammal('dog'))

    def test_hard(self):
        """ @points=2 """
        self.assertTrue(is_mammal('dolphin'))

    def test_add(self):
        """ @points=10 """
        self.assertEqual(add(2, 2), 4)
