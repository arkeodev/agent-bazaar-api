# --------- requirements ---------
FROM python:3.11-slim AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# --------- final image build ---------
FROM python:3.11

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire src directory
COPY ./src /code/src

# Create directory for Streamlit config
RUN mkdir -p /root/.streamlit

# Copy Streamlit config if exists
COPY .streamlit/config.toml /root/.streamlit/config.toml

# Add this after WORKDIR /code
ENV PYTHONPATH=/code/src:$PYTHONPATH

# -------- replace with comment to run with gunicorn --------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
