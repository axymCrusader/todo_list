# Todo List Application with FastAPI and JWT Authentication

This is a Todo List application built with FastAPI, SQLAlchemy, and JWT authentication. The application allows users to create, read, update, and delete tasks and task types. Each task is associated with a specific task type and a user. The backend uses PostgreSQL for data storage, with Alembic for database migrations. Docker Compose is utilized for managing multi-container Docker applications.


## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Create a `.env` file in the project root directory with the following environment variables:
   ```env
   DB_USER=<your_database_user>
   DB_PASSWORD=<your_database_password>
   DB_NAME=<your_database_name>
   DB_HOST=db
   DB_PORT=5432

   SENTRY_URL=<your_sentry_url>  # Optional if not to be left blank

   JWT_SECRET_KEY=<your_jwt_secret_key>
   ```

   Replace the placeholder values with your actual credentials and configuration settings.


3. Run the following command to start the containers:
   ```bash
   docker-compose up --build
   ```
   This will start the FastAPI application and PostgreSQL database containers.

4. Access the application at `http://localhost:8000`.
