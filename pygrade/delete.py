#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Delete student repositories, teams, and accounts. 

usage:
    pygrade delete --org <name> --user <username> --pass <passwd> [--students <file>]

Options
    -h, --help
    -o, --org <string>          Name of the GitHub Organization for the course.
    -p, --pass <str>           GitHub password
    -s, --students <file>       Students TSV file [default: students.tsv]
    -u, --user <str>           GitHub username
"""
from docopt import docopt
from git import Repo
from github3 import login
import os
import time
import traceback
from . import clone_repo, get_local_repo, pull_repo, read_students


def lookup_team(existing_teams, name):
    for t in existing_teams:
        if t.name == name:
            return t

def search_for_user(github, userid):
    try:
        return github.user(userid)
    except:
        print('>>>cannot find github user with login %s. skipping...' % userid)
    return None

def lookup_repo(existing_repos, name):
    for t in existing_repos:
        if t.name == name:
            return t

def delete_accounts(students, org_name, github,):
    try:
        org = [o for o in github.me().organizations() if os.path.basename(o.url) == org_name][0]
        print('found org %s' % org.url)
    except Exception as e:
        print('>>>cannot find org named %s' % org_name)
        print(str(e))
        traceback.print_exc()
        return

    existing_teams = [t for t in org.teams()]
    existing_repos = [r for r in org.repositories()]
    for s in students:
        print('deleting repo %s and account %s' % (s['github_repo'], s['github_id']))
        user = search_for_user(github, s['github_id'])
        if not user:
            print('>>>cannot find %s' % s['github_id'])
        team_name = os.path.basename(s['github_repo'])
        repo = lookup_repo(existing_repos, team_name)
        if not repo:
            print('>>>cannot get repo for %s' % s['github_repo'])
        else:
            if repo.delete():
                print('\trepo deleted')
            else:
                print('\t>>>repo deletion failed')
        time.sleep(.5)
        team = lookup_team(existing_teams, team_name)
        if not team:
            print('>>>cannot find %s' % s['github_id'])
        else:
            if team.delete():
                print('\tteam deleted')
            else:
                print('\t>>>team deletion failed')
        if org.remove_member(s['github_id']):
            print('\tremoved from org')
        else:
            print('\t>>>remove from org failed')

def main():
    args = docopt(__doc__)
    students = read_students(args['--students'])
    github = login(args['--user'], args['--pass'])
    delete_accounts(students, args['--org'], github)

if __name__ == '__main__':
    main()
