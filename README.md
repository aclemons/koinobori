# koinobori

An example FastAPI app. 🎏

## Getting Started

You need Python 3.10.11 and Poetry 1.5.0.

- `pyenv` is the simplest way to manage your python versions.
  - `pyenv install "$(cat .python-version)"`
- `poetry` can be installed through the official script
  - `curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.0 python3 -`

After installing the dependencies, setup your poetry environment:

    $ poetry env use "$(cat .python-version)"
    $ poetry install

## Dev Server

You can start running the dev server with:

    $ poetry run python3 koinobori/lambdas/api/local.py

The swagger ui will now be accessible at http://127.0.0.1:8000/docs


## Lambda Local

You need docker compose to be installed. Then you can bring up the lambda and tiny proxy to forward normal HTTP requests to the lambda:

    $ docker compose up --build

The swagger ui will now be accessible at http://127.0.0.1:8000/docs
