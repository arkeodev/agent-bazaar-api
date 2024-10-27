# Agent Bazaar

**Agent Bazaar** creates an extensible marketplace for AI agents using FastAPI, Streamlit, and PostgreSQL:

- [`FastAPI`](https://fastapi.tiangolo.com): Modern Python web framework for building APIs
- [`Streamlit`](https://streamlit.io): Python library for creating web apps
- [`PostgreSQL`](https://www.postgresql.org): The World's Most Advanced Open Source Relational Database
- [`Docker Compose`](https://docs.docker.com/compose/): For easy deployment and development

## Features

- 🏪 Agent marketplace interface
- 🔐 User authentication with JWT
- 🍪 Cookie based refresh token
- 🎨 Customizable Streamlit theming
- 🚀 FastAPI backend
- 🏬 PostgreSQL database
- 🚚 Easy running with docker compose

## Prerequisites

### Environment Setup

Create a `.env` file inside `src` directory:

```sh
touch .env
```

Inside `.env`, create the following variables:

```raw
# ------------- app settings -------------
APP_NAME="Agent Bazaar"
APP_DESCRIPTION="Your AI Agent Marketplace"
APP_VERSION="0.1"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
LICENSE_NAME="MIT"

# ------------- database -------------
POSTGRES_USER="your_postgres_user"
POSTGRES_PASSWORD="your_password"
POSTGRES_SERVER="your_server" # default "localhost", if using docker compose use "db"
POSTGRES_PORT=5432 # default "5432"
POSTGRES_DB="your_db"

# ------------- crypt -------------
SECRET_KEY= # result of openssl rand -hex 32
ALGORITHM= # pick an algorithm, default HS256
ACCESS_TOKEN_EXPIRE_MINUTES= # minutes until token expires, default 30
REFRESH_TOKEN_EXPIRE_DAYS= # days until token expires, default 7

# ------------- admin -------------
ADMIN_NAME="your_name"
ADMIN_EMAIL="your_email"
ADMIN_USERNAME="your_username"
ADMIN_PASSWORD="your_password"

# ------------- environment -------------
ENVIRONMENT="local"
```

### Docker Compose (Recommended)

Ensure you have docker and docker compose installed, then run:

```sh
docker compose up
```

This will start:

- Web application (FastAPI + Streamlit)
- PostgreSQL database

### Manual Setup

1. Install poetry:

```sh
pip install poetry
```

2.Install dependencies:

```sh
poetry install
```

3.Start PostgreSQL (if not using existing instance):

```sh
docker run -d \
    -p 5432:5432 \
    --name postgres \
    -e POSTGRES_PASSWORD=your_password \
    -e POSTGRES_USER=your_user \
    postgres
```

4.Run the application:

```sh
poetry run uvicorn src.app.main:app --reload
```

## Usage

### Accessing the Application

- Frontend (Streamlit): http://localhost:8501
- API Documentation: http://localhost:8000/docs

### Agent Configuration

Agents are configured in `src/app/streamlit/config.yaml`:

```yaml
agents:
  - name: Agent Name
    image_path: ./images/agent_image.png
```

### Authentication

The application uses JWT authentication:

- Login/Register through the Streamlit interface
- API endpoints protected with JWT tokens
- Refresh tokens handled via secure cookies

## Development

### Project Structure

```raw
├── src/
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── streamlit/      # Streamlit frontend
│   └── migrations/         # Database migrations
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

### Running Tests

```sh
poetry run pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
