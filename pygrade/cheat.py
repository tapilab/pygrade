#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check for cheating. Output file in format:
distance  file1  file2

usage:
    pygrade cheat --test <file> [--students <file>] [--output <file>] [--workdir <file>]

Options
    -h, --help
    -o, --output <file>             Output file [default: cheats.tsv]
    -s, --students <file>           Students TSV file [default: students.tsv]
    -t, --test <file>               File containing python tests for grading
    -w, --workdir <file>            Temporary directory for storing assignments [default: students]
"""
from docopt import docopt
from itertools import combinations
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from . import get_local_repo, read_assignment_metadata, read_students


def strip_comments(src):
    src = re.sub(re.compile('\"\"\".+?\"\"\"', re.DOTALL), ' ', src)
    src = re.sub(re.compile(r"\'\'\'.+?\'\'\'", re.DOTALL), ' ', src)
    src = re.sub(r'#.+', ' ', src)
    src = re.sub(re.compile(r'\n[\n\s]+', re.MULTILINE), '\n', src)
    return src


def parse_assignments(students, test_path, path):
    metadata = read_assignment_metadata(test_path)
    assignment_subpaths = metadata['files_to_test']
    strings = []
    filenames = []
    for s in students:
        repo = get_local_repo(s, path)
        for assignment_subpath in assignment_subpaths:
            fname = os.path.join(repo, assignment_subpath)
            try:
                src = '\n'.join(open(fname).readlines())
                strings.append(strip_comments(src))
                filenames.append(fname)
            except FileNotFoundError as e:
                pass
    print('read %d files' % len(strings))
    vec = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')
    X = vec.fit_transform(strings)
    return X, filenames


def compare_assignments(students, test_path, path):
    vectors, filenames = parse_assignments(students, test_path, path)
    distances = pairwise_distances(vectors, metric='cosine')
    distance_tuples = [(distances[i, j], filenames[i], filenames[j]) for i, j in combinations(range(len(filenames)), 2)]
    return sorted(distance_tuples)


def write_output(results, out_path):
    outf = open(out_path, 'w')
    for r in results:
        outf.write('%.4f\t%s\t%s\n' % (r[0], r[1], r[2]))
    outf.close()
    print('saved results in %s' % out_path)


def main():
    args = docopt(__doc__)
    path = args['--workdir']
    print('working directory=%s' % path)
    students = read_students(args['--students'])
    print('read %d students' % len(students))
    results = compare_assignments(students, args['--test'], path)
    write_output(results, args['--output'])


if __name__ == '__main__':
    main()
