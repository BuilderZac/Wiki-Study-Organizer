FROM python:3.14-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ARG KIWIX_PORT=8080

ENV KIWIX_PORT=${KIWIX_PORT}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        kiwix \
        kiwix-tools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN git clone --depth 1 \
        https://github.com/openzim/zimit.git \
        /tmp/zimit && \
    python -m pip install --no-cache-dir \
        /tmp/zimit && \
    rm -rf /tmp/zimit

RUN if [ -f /app/requirements.txt ]; then \
        python -m pip install --no-cache-dir \
        -r /app/requirements.txt; \
    fi

RUN mkdir -p /app/library

WORKDIR /app/library

EXPOSE ${KIWIX_PORT}

CMD ["python", "/app/main.py"]

