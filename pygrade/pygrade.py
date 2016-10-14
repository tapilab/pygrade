# -*- coding: utf-8 -*-
"""A command-line tool to auto-grade python assignments.

usage:
    pygrade [--help] <command> [<args>...]

The most commonly used pygrade commands are:
     cheat      Detect plagiarism.
     clone      Clone all student GitHub repositories.
     grade      Grade assignments.
     init       Initialize repositories.
     push       Push grades to student repositories.

See 'pygrade help <command>' for more information on a specific command.

"""
from subprocess import call
from docopt import docopt

from . import __version__


CMDS = ['cheat', 'clone', 'grade', 'init', 'push', 'summarize']


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
