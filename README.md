# Cookiecutter Ansible role

![TravisCI](https://travis-ci.org/fesaille/cookiecutter-ansible-role.svg?branch=master)

This role provides an *opiniated* cookiecutter template for an [ Ansible role ](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) with [Molecule](https://github.com/ansible-community/molecule) testing

**Works on progress**


## Dependencies

- [cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [gitpython](https://github.com/gitpython-developers/GitPython)
- [pre-commit](https://github.com/pre-commit/pre-commit)

Installation can be done e.g. with [**pipx**](https://github.com/pipxproject/pipx):

```bash
pipx install cookiecutter --pip-args gitpython
pipx install pre-commit
```

## Usage

```bash
cookiecutter gh:fesaille/cookiecutter-ansible-role
```

### under the hood


### Limitation

At the moment, multiple choices are [not supported](https://github.com/cookiecutter/cookiecutter/issues/1002) by cookiecutter but is planed for [V2.0](https://github.com/cookiecutter/cookiecutter/projects/3).


## Testing

