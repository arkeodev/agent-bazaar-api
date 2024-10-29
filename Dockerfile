# --------- requirements ---------
FROM python:3.11-slim AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# --------- final image build ---------
FROM python:3.11

WORKDIR /code

# Install PostgreSQL client
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire src directory and configuration files
COPY ./src /code/src
COPY ./src/alembic.ini /code/src/alembic.ini
COPY ./entrypoint.sh /code/

# Create migrations directory
RUN mkdir -p /code/migrations

RUN chmod +x /code/entrypoint.sh

# Create directory for Streamlit config
RUN mkdir -p /root/.streamlit

# Copy Streamlit config if exists
COPY .streamlit/config.toml /root/.streamlit/config.toml

ENV PYTHONPATH=/code/src:$PYTHONPATH

ENTRYPOINT ["/code/entrypoint.sh"]
