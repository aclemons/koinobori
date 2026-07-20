FROM ghcr.io/astral-sh/uv:0.11.29@sha256:eb2843a1e56fd9e30c7276ce1a52cba86e64c7b385f5e3279a0e08e02dd058fc AS uv
FROM public.ecr.aws/lambda/python:3.15.2026.07.20.08@sha256:a843a538de7d2772d637644d129db4820c27e8d9a5083f098349d77541fd70a5 AS base

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
