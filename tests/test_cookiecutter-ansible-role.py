from contextlib import contextmanager

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
    # c.exec_run("pipx ensurepath")
    # c.restart()
    # c.exec_run("pipx install pre-commit")
    # c.exec_run("pipx install cookiecutter --pip-args gitpython")
    yield c

    c.stop()


def test_python_installation(container: docker.models.containers.Container) -> None:
    """Test that python is available in the container."""

    python_version_tupled = tuple(int(p) for p in str(PYTHON_VERSION).split("."))
    res: docker.ExecResult = container.exec_run(
        f'python -c "import sys; assert sys.version_info >= {python_version_tupled}"'
    )

    assert res.exit_code == 0, f"Python version in container not {PYTHON_VERSION}"


def test_pre_commit_presence(container: docker.models.containers.Container) -> None:
    """Test if pre-commit is installed."""

    res: docker.ExecResult = container.exec_run("pre-commit --version")
    assert res.exit_code == 0, f"pre-commit not correctly or not installed in container"


def test_cookiecutter_presence(
    container: docker.models.containers.Container,
) -> None:
    """Test if cookiecutter is installed."""

    res: docker.ExecResult = container.exec_run("cookiecutter --version")
    assert (
        res.exit_code == 0
    ), f"cookiecutter not correctly or not installed in container"


def test_cookiecutter_installation(
    container: docker.models.containers.Container,
) -> None:
    """Test if role installation"""

    res: docker.ExecResult = container.exec_run(
        "cookiecutter --no-input gh:fesaille/cookiecutter-ansible-role -o /tmp/cookiecutter-role-ansible"
    )
    assert res.exit_code == 0, f"Role not correctly or not installed in container"
