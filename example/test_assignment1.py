"""
@name=example/assignment1.py
@possible_points=5
"""
import unittest
from assignment1 import *


class TestAssignment1(unittest.TestCase):
    def test_simple_1(self):
        """ @points 2 """
        self.assertTrue(is_mammal('cat'))

    def test_simple_2(self):
        """ @points 2 """
        self.assertTrue(is_mammal('dog'))

    def test_hard(self):
        """ @points 1 """
        self.assertTrue(is_mammal('dolphin'))
