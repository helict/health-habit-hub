FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN set -eux; \
    apt-get update; \
    apt-get -y upgrade; \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH="/app/src"

EXPOSE 8080

CMD ["uvicorn", "src.openapi_server.main:app", "--host", "0.0.0.0", "--port", "8080"]
