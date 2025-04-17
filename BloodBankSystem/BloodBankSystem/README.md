# Blood Bank Management System

A comprehensive web application for managing blood donations, requests, and donors.

## Features

- User authentication and role-based access control
- Donor registration and profile management
- Blood request submission and tracking
- Admin dashboard for system management
- Real-time notifications using WebSockets
- Cross-system database access

## Setup Instructions

### 1. Environment Setup

The application uses environment variables for configuration. Copy the `.env.example` file to `.env` and update the values:

```bash
cp .env.example .env
```

### 2. Database Configuration

#### Local Development (SQLite)

For local development, you can use SQLite by setting these values in your `.env` file:

```
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

#### Cross-System Access (PostgreSQL)

For a database that can be accessed from multiple systems, set up PostgreSQL:

1. Install PostgreSQL on your server
2. Create a database and user:
   ```sql
   CREATE DATABASE bloodbank_db;
   CREATE USER bloodbank_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE bloodbank_db TO bloodbank_user;
   ```
3. Update your `.env` file:
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=bloodbank_db
   DB_USER=bloodbank_user
   DB_PASSWORD=secure_password
   DB_HOST=your-database-server
   DB_PORT=5432
   ```

### 3. Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

## Accessing the System

The system will be available at http://127.0.0.1:8000/

## Cross-System Access Configuration

To make the system accessible from different machines:

1. Set up a centralized PostgreSQL database server
2. Configure all client systems to use the same database by updating their `.env` files
3. Ensure the database server is accessible from all client machines (configure firewall rules)
4. For production, consider using a proper web server like Nginx or Apache with Gunicorn/uWSGI

## Security Considerations

- Never expose your database directly to the internet
- Use a VPN or SSH tunnel for secure remote database access
- Keep your SECRET_KEY secure and different in production
- Set DEBUG=False in production
