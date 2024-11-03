FROM ghcr.io/astral-sh/uv:0.4.24@sha256:6aa62953bddbc9de3e1505d495049c8158d453e61dfbdf65c21dc8bcc954ec55 AS uv
FROM public.ecr.aws/lambda/python:3.12.2024.10.30.16@sha256:2951186769ff98c4f1acf3783d9432e40cb3b03c72aab239588b3544f647bb36 AS base

FROM base AS deps

WORKDIR /tmp/koinobori

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_SYSTEM_PYTHON=1

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install --requirement pyproject.toml --target "$LAMBDA_TASK_ROOT"

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.,target=/tmp/koinobori \
    uv build --wheel --out-dir /tmp/dist && \
    uv pip install --target "$LAMBDA_TASK_ROOT" /tmp/dist/koinobori*whl && \
    rm -rf /tmp/dist

FROM base

RUN mkdir -p /opt/extensions

COPY --from=deps "$LAMBDA_TASK_ROOT" "$LAMBDA_TASK_ROOT"
