#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Push grades to student repositories.

usage:
    pygrade push [--grades <file>] [--workdir <file>]

Options
    -h, --help
    -g, --grades <file>             JSON grades output by the grade command [default: grades.json]
    -w, --workdir <file>            Temporary directory for storing assignments [default: /tmp/pygrade]
"""
from docopt import docopt
from git import Repo
import json
import os
import re
import time
import unittest

from . import clone_repos, get_local_repo, mktmpdir


def write_grade_file(grade, grade_path):
    outf = open(grade_path, 'wt')
    outf.write('Grade: %.2f/%.2f\n' % (grade['grade'], grade['possible_points']))
    if len(grade['deductions']) > 0:
        outf.write('\n%d Deduction(s):\n\n' % len(grade['deductions']))
        for i, d in enumerate(grade['deductions']):
            outf.write('--------------\n#%d: %.2f points\nFailing test: %s\n%s--------------\n\n' %
                       (i + 1, d['points'], d['summary'], d['trace']))
    outf.close()


def push_file(repo, grade, grade_path):
    repo_obj = Repo(repo)
    index = repo_obj.index
    index.add([grade_path])
    index.commit('grade %s' % grade['assignment'])
    repo_obj.remotes[0].push()


def push_grades(grades, path):
    for g in grades:
        print('pushing grades for %s to %s' % (g['assignment'], g['student']['github_repo']))
        repo = get_local_repo(g['student'], path)
        asg_path = os.path.join(repo, re.sub(r'\/[^\/]+', '', g['assignment']))
        grade_path = os.path.join(asg_path, 'grade.txt')
        write_grade_file(g, grade_path)
        push_file(repo, g, grade_path)


def main():
    args = docopt(__doc__)
    path = mktmpdir(args['--workdir'])
    print('working directory=%s' % path)
    grades = [json.loads(s) for s in open(args['--grades'])]
    print('pushing %d grades' % (len(grades)))
    students = [g['student'] for g in grades]
    clone_repos(students, path)
    push_grades(grades, path)


if __name__ == '__main__':
    main()
