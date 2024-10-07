FROM ghcr.io/astral-sh/uv:0.4.18@sha256:7091de9df72a77bdc92d6460f09403b4bdd5b35fe54e3320e4e1cbdacf8cdd49 AS uv
FROM public.ecr.aws/lambda/python:3.12.2024.10.04.18@sha256:f5308d146329323f72af229ad795c1f7433b63953697997bfd9b7fb6871d2b97 AS base

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
