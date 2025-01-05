FROM python:3.12-slim

RUN apt update && apt install -y curl

ENV DOCKERIZE_VERSION v0.9.1

RUN apt-get install -y wget \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apt-get autoremove -yqq --purge wget && rm -rf /var/lib/apt/lists/*
# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/ /app/src

# Install any needed packages specified in pyproject.toml using uv
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir pip uv && \
    uv export -o requirements.txt --no-hashes && \
    pip install --no-cache-dir -r requirements.txt
