FROM public.ecr.aws/lambda/python:3.11.2023.07.13.17@sha256:10dbb67ede15b5fd516be87dd71c3f7968904b0b840235720486476b34ef9b67 as base

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
