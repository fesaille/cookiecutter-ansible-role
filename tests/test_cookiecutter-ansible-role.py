from contextlib import contextmanager
from pathlib import Path
from typing import Dict

import docker
import pytest

PYTHON_VERSION = 3.9


@contextmanager
@pytest.fixture(scope="module")
def container():

    client = docker.from_env()

    c = client.containers.run(
        "python:3.9",
        auto_remove=True,
        detach=True,
        mem_limit="64m",
        nano_cpus=1_000_000_000,
        tty=True,
    )

    c.exec_run("mkdir -p ~/.local.bin")

    c.exec_run(
        """cat << EOF > ~/.profile
    if [ -d "$HOME/.local/bin" ] ; then
      PATH="$HOME/.local/bin:$PATH"
      fi
    EOF"""
    )
    c.exec_run("pip install pipx pre-commit cookiecutter gitpython")
    yield c

    c.stop()


@pytest.fixture(scope="session")
def installation_dir(tmpdir_factory):
    tmp = tmpdir_factory.mktemp("cookie")
    return tmp


@pytest.fixture(scope="session")
def config():
    import json

    return json.load(Path("cookiecutter.json").open())


def test_python_installation(container: docker.models.containers.Container) -> None:
    """Is python available in the container?"""

    python_version_tupled = tuple(int(p) for p in str(PYTHON_VERSION).split("."))
    res: docker.ExecResult = container.exec_run(
        f'python -c "import sys; assert sys.version_info >= {python_version_tupled}"'
    )

    assert res.exit_code == 0, f"Python version in container not {PYTHON_VERSION}"


def test_pre_commit_presence(container: docker.models.containers.Container) -> None:
    """Is pre-commit installed?"""

    res: docker.ExecResult = container.exec_run("pre-commit --version")
    assert res.exit_code == 0, f"pre-commit not correctly or not installed in container"


def test_cookiecutter_presence(container: docker.models.containers.Container) -> None:
    """Is cookiecutter installed?"""

    res: docker.ExecResult = container.exec_run("cookiecutter --version")
    assert (
        res.exit_code == 0
    ), f"cookiecutter not correctly or not installed in container"


def test_is_role_installed(
    container: docker.models.containers.Container, installation_dir
) -> None:
    """Is role installed?"""

    res: docker.ExecResult = container.exec_run(
        f"cookiecutter --no-input gh:fesaille/cookiecutter-ansible-role -o {installation_dir}"
    )
    assert res.exit_code == 0, f"Role not correctly or not installed in container"


def test_is_git_dir(
    container: docker.models.containers.Container, installation_dir: Path, config: Dict
) -> None:
    """Is role inits a git dir?"""

    role_name = config["role_name"]
    role_dir = installation_dir / role_name

    res: docker.ExecResult = container.exec_run(f"git -C {role_dir} rev-parse")
    assert res.exit_code == 0, f"Role did not create a git dir"
