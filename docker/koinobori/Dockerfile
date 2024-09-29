FROM ghcr.io/astral-sh/uv:0.4.15@sha256:0e3e0ce333158c079541f6d59299e78b65aafff7db7111aa7f0f7f8edea520f4 AS uv
FROM public.ecr.aws/lambda/python:3.12.2024.09.13.17@sha256:0a3d34a8310dc339ea7afeb64725df5685da2e6f335dc9287cbc0cddc4a159f2 AS base

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
