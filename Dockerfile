# Stage 1: Build Dependencies
#FROM marketplace.gcr.io/google/ubuntu2404:latest AS build
FROM python:3.12-slim AS build

# Avoid interactive frontend
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y protobuf-compiler \
    ## cleanup
    && apt-get autoremove --purge  -y \
    && apt-get clean \
    && apt-get autoclean

# Install python
#RUN apt-get install -y python3.12 \
#    && apt-get install -y python3.12-venv

ARG APP_HOME=/home/app

# Create and set the working directory
WORKDIR ${APP_HOME}

# Create a virtual environment
RUN python3.12 -m venv ${APP_HOME}/.venv

# Activate the virtual environment
ENV PATH="${APP_HOME}/.venv/bin:$PATH"

# Install python libraries
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Build final image
#FROM marketplace.gcr.io/google/ubuntu2404:latest AS final
FROM python:3.12-slim AS final

ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1

# Copy the python environment
COPY --from=build /home/app /home/app

# Copy the application code
COPY app/ /home/app

# Expose the port
EXPOSE 8000

WORKDIR /home

# Run the web service on container startup.
CMD ["/home/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
