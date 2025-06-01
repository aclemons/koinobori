import contextlib
import tomllib
from pathlib import Path

import pytest

import docker


@pytest.fixture
def dot_python_version() -> str:
    python_version_file = Path(__file__).parent.parent / ".python-version"

    with python_version_file.open() as f:
        return f.readline().rstrip()


@pytest.fixture
def pyproject_toml_python_version() -> str:
    pyproject_toml = Path(__file__).parent.parent / "pyproject.toml"

    with pyproject_toml.open() as f:
        data = tomllib.loads(f.read())

        return data["project"]["requires-python"].removeprefix("==")


@pytest.fixture
def docker_python_version() -> str:
    dockerfile = Path() / "docker" / "koinobori" / "Dockerfile"

    image_name = "public.ecr.aws/lambda/python"
    with dockerfile.open() as f:
        lines = [line.rstrip() for line in f.readlines() if image_name in line]

    assert len(lines) == 1

    image = lines[0].split("AS", 1)[0].strip().split(" ", 1)[-1]

    with contextlib.closing(docker.from_env()) as docker_client:
        log = docker_client.containers.run(
            image=image,
            entrypoint="/bin/bash",
            command="-c 'python3 --version'",
            remove=True,
        )

    assert isinstance(log, bytes)
    return log.decode("utf-8").rstrip().split(" ", 1)[-1]


def test_python_versions_match(
    dot_python_version: str,
    docker_python_version: str,
    pyproject_toml_python_version: str,
) -> None:
    assert dot_python_version == docker_python_version
    assert dot_python_version == pyproject_toml_python_version
