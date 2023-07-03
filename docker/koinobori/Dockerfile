FROM public.ecr.aws/lambda/python:3.11-preview.2023.07.03.13@sha256:ccb372a08397bfec1bf1bc476a78a83a39d9ffb24d1e1157be7d0cb3f2d32b59 as base

FROM base as deps

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock ./

RUN export PATH="/opt/poetry/bin:$PATH" && \
    export POETRY_HOME="/opt/poetry" && \
    export POETRY_VERSION=1.5.1 && \
    curl -sSL https://install.python-poetry.org -o poetry-installer && \
    <poetry-installer python3 - && \
    poetry export --format=requirements.txt --output requirements.txt && \
    <poetry-installer python3 - --uninstall && \
    rm poetry-installer && \
    rm -r /root/.cache && \
    pip3 install --no-cache-dir --requirement requirements.txt --target "$LAMBDA_TASK_ROOT" && \
    rm requirements.txt && \
    rm pyproject.toml poetry.lock


FROM base

RUN mkdir -p /opt/extensions

COPY --from=deps "$LAMBDA_TASK_ROOT" "$LAMBDA_TASK_ROOT"

COPY koinobori "$LAMBDA_TASK_ROOT/koinobori"
