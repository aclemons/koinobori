# koinobori

An example FastAPI app. 🎏

## Getting Started

You need Python 3.11.3 and Poetry 1.5.0.

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

## Migrations

You need to create your local table in dynamodb. If you have started your local containers with docker compose as above, you can use something like [ddbsh](https://github.com/awslabs/dynamodb-shell):

    $ DDBSH_ENDPOINT_OVERRIDE=http://localhost:4566 AWS_DEFAULT_REGION=eu-central-1 ddbsh
    ddbsh - version 0.6.1
    eu-central-1 (*)> create table koinobori-local-migrations(version_num string) primary key (version_num hash);
    CREATE

You can invoke the migrations lambda with:

    $ curl "http://localhost:9002/2015-03-31/functions/function/invocations" -d '{}'
