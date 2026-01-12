FROM ghcr.io/astral-sh/uv:0.9.21@sha256:15f68a476b768083505fe1dbfcc998344d0135f0ca1b8465c4760b323904f05a AS uv
FROM public.ecr.aws/lambda/python:3.14.2026.01.09.10@sha256:8fc63f656b0907dd77dd8158e807302ebffc081b82544f46cd97bd56a3af85a0 AS base

FROM base AS deps

WORKDIR /tmp/koinobori

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_SYSTEM_PYTHON=1

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv export --no-emit-workspace --no-dev --format requirements-txt --frozen --output-file requirements.txt --quiet && \
    uv pip install --requirements requirements.txt --target "$LAMBDA_TASK_ROOT" && \
    rm requirements.txt

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.,target=/tmp/koinobori \
    uv build --wheel --out-dir /tmp/dist && \
    uv pip install --no-deps --target "$LAMBDA_TASK_ROOT" /tmp/dist/*whl && \
    rm -rf /tmp/dist

FROM base

RUN mkdir -p /opt/extensions

COPY --from=deps "$LAMBDA_TASK_ROOT" "$LAMBDA_TASK_ROOT"
