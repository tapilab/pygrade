# -*- coding: utf-8 -*-

__author__ = 'Aron Culotta'
__email__ = 'aronwc@gmail.com'
__version__ = '0.1.0'

import csv
import errno
import git
import os
import re
import time
import traceback


def extract_metadata(text, result):
    """
    >>> extract_metadata('@name=a0/foo.py...', {})['file_to_test']
    'a0/foo.py'
    >>> extract_metadata('@possible_points=12.4', {})['possible_points']
    12.4
    """
    match = re.search(r'\@name\s*=\s*(.+.py)', text)
    if match:
        result['file_to_test'] = match.group(1)
    match = re.search(r'\@possible_points\s*=\s*([0-9\.]+)', text)
    if match:
        result['possible_points'] = float(match.group(1))
    return result


def read_assignment_metadata(test_file):
    """
    Extracts metadata in the comments of the unit test file. E.g.:
    @name=a0/boolean_search.py
    @possible_points=50
    """
    result = {'file_to_test': None,
              'possible_points': None}

    for line in open(test_file):
        extract_metadata(line, result)
    return result


def check_students(students):
    """ Make sure we have requisite fields for each student. """
    for s in students:
        if 'github_repo' not in s:
            print('missing github_repo for %s' % str(s))


def read_students(path):
    """ Read a tab-separated file of students. The only required field is 'github_repo', which is this
    student's github repository. """
    students = [line for line in csv.DictReader(open(path), delimiter='\t')]
    check_students(students)
    return students


def path2name(path):
    """ Get the basename of a file, minus any extensions.
    >>> path2name('foo/bar/baz.py')
    'baz'
    """
    return re.sub(r'\..+', '', os.path.basename(path))


def get_local_repo(s, path):
    """ Return the path to the local copy of this student's repository. """
    return os.path.join(path, os.path.basename(s['github_repo']))


def clone_repos(students, path):
    """ Clone all student repos. """
    for s in students:
        repo = s['github_repo']
        topath = get_local_repo(s, path)
        print('cloning %s to %s ...' % (repo, topath))
        git.repo.base.Repo.clone_from(repo + '.git', topath)


def mktmpdir(subdir):
    """ Make a unique, temporary directory for student repos. """
    path = '%s-%d' % (subdir, time.time())
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
    return path
