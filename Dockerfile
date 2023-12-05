FROM python:3.12.0-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc

COPY ./__main__.py /app/__main__.py
COPY ./src /app/src

CMD ["/opt/venv/bin/python", "__main__.py"]
