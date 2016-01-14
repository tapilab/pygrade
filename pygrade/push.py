#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Push grades to student repositories.

usage:
    pygrade push [--grades <file>] [--workdir <file>]

Options
    -h, --help
    -g, --grades <file>             JSON grades output by the grade command [default: grades.json]
    -w, --workdir <file>            Temporary directory for storing assignments [default: students]
"""
from docopt import docopt
from git import Repo
import json
import os

from . import get_local_repo


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
        repo = get_local_repo(g['student'], path)
        asg_path = os.path.dirname(g['assignment'][0])
        grade_path = os.path.join(repo, asg_path, 'grade.txt')
        write_grade_file(g, grade_path)
        print('pushing grade %s to %s' % (grade_path, g['student']['github_repo']))
        push_file(repo, g, os.path.join(asg_path, 'grade.txt'))


def main():
    args = docopt(__doc__)
    path = args['--workdir']
    grades = [json.loads(s) for s in open(args['--grades'])]
    print('pushing %d grades' % (len(grades)))
    push_grades(grades, path)


if __name__ == '__main__':
    main()
