#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Grade a Python assignment.

usage:
    pygrade grade --students <file> --test <file> [--output <file>] [--workdir <file>]

Options
    -h, --help
    -s, --students <file>           Students JSON file
    -t, --test <file>               File containing python tests for grading
    -o, --output <file>             Output file [default: grades.json]
    -w, --workdir <file>            Temporary directory for storing assignments [default: /tmp/pygrade]
"""
import csv
from docopt import docopt
import importlib
import json
import os
import re
import time
import unittest

from . import clone_repos, get_local_repo, path2name, mktmpdir, read_students


def read_assignment_metadata(test_file):
    """
    Extracts metadata in the comments of the unit test file. E.g.:
    @name=a0/boolean_search.py
    @points=50
    """
    result = {'file_to_test': None,
              'points': None}

    for line in open(test_file):
        match = re.search(r'\@name\s*=\s*(.+.py)', line)
        if match:
             result['file_to_test'] = match.group(1)
        match = re.search(r'\@points\s*=\s*([0-9\.]+)', line)
        if match:
            result['points'] = float(match.group(1))
    return result


def import_file_as_module(path):
    """ Return a python file as a module. """
    module_name = path2name(path)
    loader = importlib.machinery.SourceFileLoader(module_name, path)
    return loader.load_module()


def _run_tests(test_path):
    """ Run the unit tests in this file and return the results. """
    test_module = import_file_as_module(test_path)
    suite = unittest.TestLoader().loadTestsFromModule(test_module)
    test_results = unittest.TestCase().defaultTestResult()
    return suite.run(test_results)


def deduct_failures(test_results):
    """ Accumulate each failed tests and the points lost."""
    deductions = []
    for failure in test_results.failures:
        msg = failure[1]
        match = re.search(r'\: ([0-9\.]+)\s*$', msg)
        points = float(match.group(1)) if match else 0
        deduction = {'summary': '%s%s' % (failure[0]._testMethodName,
                                          ': ' + failure[0]._testMethodDoc
                                          if failure[0]._testMethodDoc else ''),
                     'trace': msg,
                     'points': points}
        deductions.append(deduction)
    return deductions


def run_tests(students, test_path, path):
    """
    Run unit tests and deduct points for each failed test.
    Return a dictionary of results for each student.
    FIXME: check for errors?
    """
    metadata = read_assignment_metadata(test_path)
    assignment_subpath = metadata['file_to_test']
    results = []
    for s in students:
        result = {'student': s, 'assignment': assignment_subpath,
                  'time_graded': time.asctime(),
                  'possible_points': metadata['points']}
        repo = get_local_repo(s, path)
        assignment_path = os.path.join(repo, assignment_subpath)
        try:
            assignment_module = import_file_as_module(assignment_path)
        except Exception as e:  # Can't load the student's homework file.
            result['deductions'] = [{'summary': 'cannot import %s' % assignment_subpath,
                                     'trace': str(e),
                                     'points': metadata['points']}]
            result['grade'] = 0
            results.append(result)
            continue
        test_results = _run_tests(test_path)
        result['deductions'] = deduct_failures(test_results)
        result['grade'] = max(0, metadata['points'] - sum(d['points'] for d in result['deductions']))
        results.append(result)
    return results


def main():
    args = docopt(__doc__)
    path = mktmpdir(args['--workdir'])
    print('working directory=%s' % path)
    students = read_students(args['--students'])
    print('read %d students' % len(students))
    clone_repos(students, path)
    results = run_tests(students, args['--test'], path)
    json.dump(results, open(args['--output'], 'w'), sort_keys=True, ensure_ascii=False, indent=2)
    print('saved results in %s' % args['--output'])

if __name__ == '__main__':
    main()
