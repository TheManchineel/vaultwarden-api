FROM python:3.10-alpine as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.6.1

COPY . .
RUN apk add --no-cache gcc libffi-dev musl-dev && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry install --no-dev --no-root && \
    poetry build

FROM base as final
COPY --from=builder /app/dist /app/dist
RUN pip install /app/dist/*.whl
CMD ["uvicorn", "vaultwarden_api:app", "--port", "8019", "--host", "0.0.0.0"]