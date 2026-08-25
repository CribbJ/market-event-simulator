FROM python:3.13-slim

WORKDIR /marketsimulator

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "marketsimulator"]
CMD []