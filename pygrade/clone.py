#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Clone student GitHub repositories.

usage:
    pygrade clone [--students <file>] [--workdir <file>]

Options
    -h, --help
    -s, --students <file>           Students JSON file [default: students.tsv]
    -w, --workdir <file>            Temporary directory for storing assignments [default: students]
"""
from docopt import docopt
from . import clone_repos, mktmpdir, read_students


def main():
    args = docopt(__doc__)
    # path = mktmpdir(args['--workdir']) if args['--workdir'] == '/tmp/pygrade' else args['--workdir']
    path = args['--workdir']
    print('working directory=%s' % path)
    students = read_students(args['--students'])
    print('read %d students' % len(students))
    clone_repos(students, path)


if __name__ == '__main__':
    main()
