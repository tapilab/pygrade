#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Delete student repositories, teams, and accounts. 

usage:
    pygrade init --org <name> --user <username> --pass <passwd> --remote <uri> [--students <file>] [--workdir <file>]

Options
    -h, --help
    -o, --org <string>          Name of the GitHub Organization for the course.
    -p, --pass <file>           GitHub password
    -s, --students <file>       Students TSV file [default: students.tsv]
    -u, --user <file>           GitHub username
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


def get_team(team_name, existing_teams, org, user):
    team = lookup_team(existing_teams, team_name)
    if not team:
        try:
            print('creating team for %s' % team_name)
            team = org.create_team(team_name, permission='push')
            print('  created new team %s' % team.name)
            team.invite(user.login)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
    else:
        print('  found existing team %s' % team.name)

    return team


def lookup_repo(existing_repos, name):
    for t in existing_repos:
        if t.name == name:
            return t


def get_repo(repo_name, existing_repos, org, team):
    repo = lookup_repo(existing_repos, repo_name)
    if not repo:
        try:
            repo = org.create_repository(repo_name, team_id=team.id, private=True, auto_init=False)
            print('  created new repo %s' % repo.name)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
    else:
        print('  found existing remote repo %s' % repo.name)

    return repo


def add_to_org(user, org):
    org.add_to_members(user, role='member')


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
            print('cannot find %s' % s['github_id'])
            continue
        team_name = os.path.basename(s['github_repo'])
        team = get_team(team_name, existing_teams, org, user)
        if not team:
            print('cannot find %s' % s['github_id'])
        repo = get_repo(team_name, existing_repos, org, team)
        time.sleep(1)
        if not repo:
            print('cannot get repo for %s' % s['github_repo'])


def write_readme(student, local_repo):
    reamde_file = os.path.join(local_repo, 'Info.md')
    outf = open(reamde_file, 'wt')
    outf.write('\n'.join('%s=%s  ' % (k, v) for k, v in student.items()))
    outf.close()


def push_readme(repo):
    repo_obj = Repo(repo)
    index = repo_obj.index
    index.add(['Info.md'])
    index.commit('Info')
    repo_obj.remotes[0].push()
    print('  pushed Info.md')


def add_remote(local_repo, remote_repo):
    repo_obj = Repo(local_repo)
    try:
        repo_obj.create_remote('template', remote_repo)
    except:  # remote already exists
        pass
    repo_obj.git.fetch('template')
    repo_obj.git.merge('template/master', allow_unrelated_histories=True)
    repo_obj.remotes[0].push()
    print('  pushed template from remote %s' % remote_repo)


def main():
    args = docopt(__doc__)
    students = read_students(args['--students'])
    github = login(args['--user'], args['--pass'])
    delete_accounts(students, args['--org'], github)

if __name__ == '__main__':
    main()
