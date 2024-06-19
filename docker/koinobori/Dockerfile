FROM public.ecr.aws/lambda/python:3.12.2024.06.18.16@sha256:91ed051a27a1e27729351258358dfdf6622af136aeb50bd75d3bbf6ab790afdd as base

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
