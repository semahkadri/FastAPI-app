# FastAPI App 🚀

This repository contains a FastAPI application with Docker Compose setup for a PostgreSQL database and pgAdmin.

## Docker Compose 🐳

### Services 🛠️

- **postgres-container**: PostgreSQL database container.
- **pgadmin**: pgAdmin container for database management.
- **fastapi**: FastAPI application container.

### Ports 🌐

- **PostgreSQL**: 5432
- **pgAdmin**: 8888
- **FastAPI**: 8000

### Environment Variables 🧪

- **PostgreSQL**:
  - POSTGRES_USER: semah
  - POSTGRES_PASSWORD: semah

- **pgAdmin**:
  - PGADMIN_DEFAULT_EMAIL: semah@gmail.com
  - PGADMIN_DEFAULT_PASSWORD: semah

## Dockerfile 🐋

The Dockerfile sets up the FastAPI application.

## main.py 🚦

The main FastAPI application code.

## requirements.txt 📋

Dependencies for the FastAPI application.

## Usage 🚀

1. Clone the repository: git clone https://github.com/semahkadri/FastAPI-app.git

2. Navigate to the project directory: cd FastAPI-app

3. Build and run the Docker containers: docker-compose up --build

4. Access FastAPI at http://localhost:8000.

5. Access pgAdmin at http://localhost:8888 with credentials:
   - Email: semah@gmail.com
   - Password: semah
