#!/usr/bin/env python

from pathlib import Path
from git import Repo

# Init the repo as git directory
if "{{ cookiecutter.init_git }}" == "y":
    repo = Repo.init('.')

if "{{ cookiecutter.add_travis_config }}" == "n":
    Path(".travis.yml").unlink()

if "{{ cookiecutter.add_gitlab_ci_config }}" == "n":
    Path(".gitlab-ci.yml").unlink()

if "{{ cookiecutter.add_gitlab_ci_config }}" == "n":
    Path(".gitlab-ci.yml").unlink()


