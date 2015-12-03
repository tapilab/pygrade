# -*- coding: utf-8 -*-

__author__ = 'Aron Culotta'
__email__ = 'aronwc@gmail.com'
__version__ = '0.1.0'

import errno
import git
import os
import re
import time
import traceback


def path2name(path):
    """ Get the basename of a file, minus any extensions. """
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
