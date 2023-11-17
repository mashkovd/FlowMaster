# Use an official Python runtime as a parent image
FROM python:3.9.16-slim-buster

# Set metadata and label
LABEL author="Dmitrii Mahkov"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y git ssh curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true

# Copy only the dependency files to leverage Docker caching
COPY ./pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Set the default command to run the application
CMD ["poetry", "run", "python", "app.py", "-A", "app", "worker", "-l", "info", "--web-port", "8000"]
