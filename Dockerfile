FROM webrecorder/browsertrix-crawler:1.15.2

LABEL org.opencontainers.image.source=https://github.com/openzim/zimit

USER root

ENV DEBIAN_FRONTEND=noninteractive

ARG KIWIX_PORT=38273
ENV KIWIX_PORT=${KIWIX_PORT}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        libcairo2 \
        libmagic1 \
        kiwix \
        kiwix-tools \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv using the Python already supplied by Browsertrix.
RUN python3 -m pip install \
        --break-system-packages \
        --no-cache-dir \
        uv

# Install Python 3.14 and Zimit from the current upstream source.
RUN git clone --depth 1 \
        https://github.com/openzim/zimit.git \
        /tmp/zimit && \
    uv venv --python 3.14 /opt/zimit && \
    uv pip install \
        --python /opt/zimit/bin/python \
        /tmp/zimit && \
    rm -rf /tmp/zimit

ENV PATH="/opt/zimit/bin:${PATH}"

COPY . /app

RUN if [ -f /app/requirements.txt ]; then \
        uv pip install \
        --python /opt/zimit/bin/python \
        -r /app/requirements.txt; \
    fi

RUN mkdir -p /app/library

WORKDIR /app/library

EXPOSE ${KIWIX_PORT}

ENTRYPOINT []

#CMD ["/bin/bash"]
#CMD ["python3", "/app/main.py"]

