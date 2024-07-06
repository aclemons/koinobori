FROM public.ecr.aws/lambda/python:3.12.2024.07.04.13@sha256:af2ab554b10207afdbab1084cdfe087b827f6c76b461ed0a1d806aed508222eb as base

FROM base as deps

WORKDIR /tmp

ENV PATH="/opt/poetry/bin:$PATH"

RUN export POETRY_HOME="/opt/poetry" && \
    export POETRY_VERSION=1.8.3 && \
    curl -sSL https://install.python-poetry.org -o poetry-installer && \
    <poetry-installer python3 - && \
    poetry self add poetry-plugin-export==1.8.0 && \
    rm poetry-installer

COPY ./pyproject.toml ./poetry.lock ./

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3041,SC2046
RUN poetry export --format=requirements.txt --output requirements.txt && \
    rm -r /root/.cache && \
    pip3 install --no-cache-dir --requirement requirements.txt --target "$LAMBDA_TASK_ROOT" && \
    rm requirements.txt && \
    rm pyproject.toml poetry.lock


FROM base

RUN mkdir -p /opt/extensions

COPY --from=deps "$LAMBDA_TASK_ROOT" "$LAMBDA_TASK_ROOT"

COPY koinobori "$LAMBDA_TASK_ROOT/koinobori"
