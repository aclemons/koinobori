FROM public.ecr.aws/lambda/python:3.12.2024.04.17.17@sha256:3df8dcffd27efbaa191051cd2247e07e4a86aac394c6644e717cda3ca407f212 as base

FROM base as deps

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock ./

# hadolint ignore=DL3041
RUN export PATH="/opt/poetry/bin:$PATH" && \
    export POETRY_HOME="/opt/poetry" && \
    export POETRY_VERSION=1.8.3 && \
    curl -sSL https://install.python-poetry.org -o poetry-installer && \
    <poetry-installer python3 - && \
    poetry self add poetry-plugin-export==1.7.1 && \
    poetry export --format=requirements.txt --output requirements.txt && \
    <poetry-installer python3 - --uninstall && \
    rm poetry-installer && \
    rm -r /root/.cache && \
    dnf install -y gcc && \
    pip3 install --no-cache-dir --requirement requirements.txt --target "$LAMBDA_TASK_ROOT" && \
    rm requirements.txt && \
    rm pyproject.toml poetry.lock && \
    dnf clean all


FROM base

RUN mkdir -p /opt/extensions

COPY --from=deps "$LAMBDA_TASK_ROOT" "$LAMBDA_TASK_ROOT"

COPY koinobori "$LAMBDA_TASK_ROOT/koinobori"
