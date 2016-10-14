#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Summarize grades.

usage:
    pygrade summarize [--grades <file>] [--test-names <names>] [--student-names <names>]

Options
    -h, --help
    -g, --grades <file>              JSON grades output by the grade command [default: grades.json]
    -t, --test-names <names>         Comma-separated list of test names to summarize.
    -s, --student-names <names>      Comma-separated list of student github ids to summarize.
"""
from collections import Counter, defaultdict
from docopt import docopt
import json
import re


def print_grade_distribution(grades):
    print('\n\n----------------------------\ngrade distribution:\ngrade\tcount\tstudents')
    counts = Counter(float(g['grade']) for g in grades)
    grade2students = defaultdict(lambda: [])
    for g in grades:
        grade2students[g['grade']].append(g['student']['github_id'])
    for grade, count in sorted(counts.items(), reverse=True):
        if count < 10:
            print('%d\t%d\t%s' % (grade, count, ' '.join(grade2students[grade])))
        else:
            print('%d\t%d' % (grade, count))


def clean_summary(s):
    return s[:s.index(':')]


def print_test_distribution(grades):
    print('\n\n----------------------------\ntest failures distribution:\n%20s\tcount\tstudents' % 'test')
    counts = Counter()
    test2students = defaultdict(lambda: [])
    for g in grades:
        counts.update(clean_summary(d['summary']) for d in g['deductions'])
        for d in g['deductions']:
            test2students[clean_summary(d['summary'])].append(g['student']['github_id'])

    for test, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        if count < 10:
            print('%20s\t%d\t%s' % (test, count, ' '.join(test2students[test])))
        else:
            print('%20s\t%d' % (test, count))

def extract_error(trace):
    re.find('.*([A-Za-z]Error:.+)$', trace)

def summarize_errors(grades, test_names):
    test_names = set([s.strip() for s in test_names.split(',')])
    test2error_counts = defaultdict(lambda: Counter())
    error2students = defaultdict(lambda: [])
    for g in grades:
        for d in g['deductions']:
            test_name = clean_summary(d['summary'])
            if test_name in test_names:
                trace = d['trace']
                text = trace[:trace.index('source:')].strip()
                test2error_counts[test_name].update([text])
                error2students[test_name + '__' + text].append(g['student']['github_id'])
    for test, error_counts in sorted(test2error_counts.items()):
        print('\n\n----------------------------\nSummary of errors for test %s\n' % test)
        for error, count in sorted(error_counts.items(), key=lambda x: -x[1]):
            print('count=%d' % count)
            print('students=%s' % ' '.join(error2students[test + '__' + error]))
            print(error)
            print('\n')


def summarize_students(grades, student_names):
    student_names = set([s.strip() for s in student_names.split(',')])
    for g in grades:
        if g['student']['github_id'] in student_names:
            print('\n\n----------------------------\nSummary of errors for student %s\n' % g['student']['github_id'])
            for d in g['deductions']:
                print('\n%d points deducted for %s' % (d['points'], clean_summary(d['summary'])))
                print(d['trace'])

def main():
    args = docopt(__doc__)
    grades = [json.loads(s) for s in open(args['--grades'])]
    print_grade_distribution(grades)
    print_test_distribution(grades)
    if args['--test-names']:
        summarize_errors(grades, args['--test-names'])
    if args['--student-names']:
        summarize_students(grades, args['--student-names'])

if __name__ == '__main__':
    main()
