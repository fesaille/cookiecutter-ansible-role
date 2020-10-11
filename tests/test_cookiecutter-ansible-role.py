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
    c.exec_run("pip install pipx")
    c.exec_run("pipx install pre-commit")
    c.exec_run("pipx install cookiecutter --pip-args gitpython")
    yield c

    c.stop()


def test_python_availability(container: docker.models.containers.Container) -> None:
    """Test that python is available in the container."""

    python_version_tupled = tuple(int(p) for p in str(PYTHON_VERSION).split("."))
    res: docker.ExecResult = container.exec_run(
        f'python -c "import sys; assert sys.version_info >= {python_version_tupled}"'
    )

    assert res.exit_code == 0, f"Python version in container not {PYTHON_VERSION}"
