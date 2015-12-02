# -*- coding: utf-8 -*-
"""A command-line tool to auto-grade python assignments.

usage:
    pygrade [--help] <command> [<args>...]

The most commonly used pygrade commands are:
     grade      Grade assignments
     cheat      Detect plagiarism

See 'pygrade help <command>' for more information on a specific command.

"""
from subprocess import call
from docopt import docopt

from . import __version__


CMDS = ['grade', 'cheat']


def clone(repo):
    pass

def run_tests(repo, assignment_file, test_file):
    pass

def report_results():
    pass


def main():
    args = docopt(__doc__,
                  version='pygrade version ' + __version__,
                  options_first=True)

    argv = [args['<command>']] + args['<args>']
    if args['<command>'] in CMDS:
        exit(call(['pygrade-%s' % args['<command>']] + argv))
    elif args['<command>'] in ['help', None]:
        exit(call(['pygrade', '--help']))
    else:
        exit("%r is not a pygrade command. See 'pygrade help'." % args['<command>'])

if __name__ == '__main__':
    main()
