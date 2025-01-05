FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/ /app/src

# Install any needed packages specified in pyproject.toml using uv
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir pip uv && \
    uv export -o requirements.txt --no-hashes && \
    pip install --no-cache-dir -r requirements.txt
