#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize student repositories. Create one repo per student. Also create one team per student consisting of that student. Each repo is made private to that team.

usage:
    pygrade init --org <name> --user <username> --pass <passwd> [--students <file>] [--workdir <file>]

Options
    -h, --help
    -o, --org <string>          Name of the GitHub Organization for the course.
    -p, --pass <file>           GitHub password
    -s, --students <file>       Students JSON file [default: students.tsv]
    -u, --user <file>           GitHub username
    -w, --workdir <file>        Temporary directory for storing assignments [default: students]
"""
from docopt import docopt
from git import Repo
from github import Github
import os
import traceback
from . import clone_repo, get_local_repo, read_students


def lookup_team(existing_teams, name):
    for t in existing_teams:
        if t.name == name:
            return t


def search_for_user(github, userid):
    for r in github.search_users('%s in:login' % userid):
        if r.login.lower() == userid.lower().strip():
            return r
    print('>>>cannot find github user with login %s. skipping...' % userid)
    return None


def get_team(team_name, existing_teams, org, user):
    team = lookup_team(existing_teams, team_name)
    if not team:
        try:
            team = org.create_team(team_name, permission='push')
            print('  created new team %s' % team.name)
            team.add_membership(user)
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
            repo = org.create_repo(repo_name, team_id=team, private=True)
            print('  created new repo %s' % repo.name)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
    else:
        print('  found existing repo %s' % repo.name)

    return repo


def add_to_org(user, org):
    org.add_to_members(user, role='member')


def create_repos_and_teams(students, org_name, github, path):
    try:
        org = [o for o in github.get_user().get_orgs() if os.path.basename(o.url) == org_name][0]
        print('found org %s' % org.url)
    except Exception as e:
        print('>>>cannot find org named %s' % org_name)
        print(str(e))
        traceback.print_exc()

    existing_teams = [t for t in org.get_teams()]
    existing_repos = [r for r in org.get_repos()]
    for s in students:
        print('initializing repo %s for %s' % (s['github_repo'], s['github_id']))
        user = search_for_user(github, s['github_id'])
        # add_to_org(user, org)
        if not user:
            next
        team_name = os.path.basename(s['github_repo'])
        team = get_team(team_name, existing_teams, org, user)
        if not team:
            next
        repo = get_repo(team_name, existing_repos, org, team)
        local_repo = get_local_repo(s, path)
        if clone_repo(s, path):
            readme_path = write_readme(s, local_repo)
            push_readme(local_repo)
        else:
            print('repo already exists in path %s' % local_repo)


def write_readme(student, local_repo):
    reamde_file = os.path.join(local_repo, 'README.md')
    outf = open(reamde_file, 'wt')
    outf.write('\n\n'.join('%s=%s' % (k, v) for k, v in student.items()))
    outf.close()


def push_readme(repo):
    repo_obj = Repo(repo)
    index = repo_obj.index
    index.add(['README.md'])
    index.commit('README')
    repo_obj.remotes[0].push()
    print('  pushed README.md')


def main():
    args = docopt(__doc__)
    path = args['--workdir']
    students = read_students(args['--students'])
    github = Github(args['--user'], args['--pass'])
    create_repos_and_teams(students, args['--org'], github, path)

if __name__ == '__main__':
    main()
