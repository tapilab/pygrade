#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Grade a Python assignment.

usage:
    pygrade grade --students <file> --test <file> --output <file> [--workdir <file>]

Options
    -h, --help
    -s, --students <file>           Students JSON file
    -t, --test <file>               File containing python tests for grading
    -o, --output <file>             Output file
    -w, --workdir <file>            Temporary directory for storing assignments [default: /tmp/pygrade]
"""
import csv
from docopt import docopt
import errno
import git
import importlib
import os
import re
import time
import unittest

from . import __version__


def get_local_repo(s, path):
    return os.path.join(path, os.path.basename(s['github_repo']))


def clone_repos(students, path):
    """ Clone all student repos. """
    for s in students:
        repo = s['github_repo']
        topath = get_local_repo(s, path)
        print('cloning %s to %s ...' % (repo, topath))
        git.repo.base.Repo.clone_from(repo + '.git', topath)


def read_assignment_metadata(test_file):
    result = {'file_to_test': None,
              'points': None}

    for line in open(test_file):
        match = re.search(r'\@name\s*=\s*(.+.py)', line)
        if match:
             result['file_to_test'] = match.group(1)
        match = re.search(r'\@points\s*=\s*([0-9\.]+)', line)
        if match:
            result['points'] = match.group(1)
    return result


def path2name(path):
    return re.sub(r'\..+', '', os.path.basename(path))


def import_file_as_module(path):
    module_name = path2name(path)
    print('importing %s from %s' % (module_name, path))
    loader = importlib.machinery.SourceFileLoader(module_name, path)
    return loader.load_module()


def run_tests(students, test_path, path):
    metadata = read_assignment_metadata(test_path)
    assignment_subpath = metadata['file_to_test']
    results = []
    for s in students:
        result = {'student': s, 'assignment': assignment_subpath, 'time_graded': time.asctime()}
        repo = get_local_repo(s, path)
        assignment_path = os.path.join(repo, assignment_subpath)
        try:
            assignment_module = import_file_as_module(assignment_path)
        except Exception as e:
            print('cannot find assignment file %s' % assignment_path)
            result['deductions'] = [('cannot import %s' % assignment_path, metadata['points'])]
            results.append(result)
            continue
        print('assignment module: %s' % str(assignment_module))
        test_module = import_file_as_module(test_path)
        print('test module: %s' % (str(test_module)))
        suite = unittest.TestLoader().loadTestsFromModule(test_module)
        test_results = unittest.TestCase().defaultTestResult()
        test_results = suite.run(test_results)
        print(test_results)
        print(dir(test_results))
        for failure in test_results.failures:
            print('failure: %s\n%s' % (failure[1], dir(failure[0])))
    return results

def report_results():
    pass


def mktmpdir(subdir):
    """ Make a unique, temporary directory for student repos. """
    path = '%s-%d' % (subdir, time.time())
    try:
        os.makedirs(path)
    except OSError as e:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
    return path


def read_students(path):
    """ Read a tab-separated file of students. The only required field is 'github_repo', which is this
    student's github repository. """
    return [line for line in csv.DictReader(open(path), delimiter='\t')]


def check_students(students):
    """ Make sure we have requisite fields for each student."""
    for s in students:
        if 'github_repo' not in s:
            print('missing github_repo for %s' % str(s))


def main():
    args = docopt(__doc__)
    path = mktmpdir(args['--workdir'])
    print('working directory=%s' % path)
    students = read_students(args['--students'])
    print('read %d students' % len(students))
    check_students(students)
    clone_repos(students, path)
    results = run_tests(students, args['--test'], path)
    print(results)

if __name__ == '__main__':
    main()
