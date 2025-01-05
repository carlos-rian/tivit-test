FROM python:3.12-slim

RUN apt update && apt install -y curl

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/ /app/src

# Install any needed packages specified in pyproject.toml using uv
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir pip uv && \
    uv export -o requirements.txt --no-hashes && \
    pip install --no-cache-dir -r requirements.txt


RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh
