# Django Project with Docker

This project uses Docker to containerize a Django application with a PostgreSQL database, supporting both local development and production environments.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

```plaintext
.
├── app/                          # Django project files
│   ├── config/                   # Django settings
│   ├── manage.py                 # Django management script
├── Dockerfile                    # Docker configuration for building the web service
├── docker-compose.yml            # Docker Compose configuration
├── .env.local                    # Environment variables for local development
├── .env.production               # Environment variables for production
└── README.md                     # Documentation
```

## Environment Variables

### Local Development

Create a `.env.local` file in the project root and add the following variables for local development:

```env
DEBUG=True
DATABASE_NAME=your_local_db_name
DATABASE_USER=your_local_db_user
DATABASE_PASSWORD=your_local_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

### Production

Create a `.env.production` file in the project root with your production settings:

```env
DEBUG=False
DATABASE_NAME=your_production_db_name
DATABASE_USER=your_production_db_user
DATABASE_PASSWORD=your_production_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

**Note**: Make sure not to commit sensitive information like `.env.production` to version control.

## Docker Setup

### Dockerfile

The `Dockerfile` defines the setup for your Django application container:

```dockerfile
# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Docker Compose

The `docker-compose.yml` file defines the configuration for both the web and database services:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env.local  # Change to .env.production for production
    depends_on:
      - db

  db:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_DB: ${DATABASE_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Running the Project

### Local Development

To start the project in local development mode:

1. Ensure you have created and configured `.env.local`.
2. Build and start the Docker containers:

   ```bash
   docker-compose --env-file .env.local up --build
   ```

   This command will start the Django development server on `http://localhost:8000`.

### Production Environment

To start the project in production mode:

1. Ensure you have created and configured `.env.production`.
2. Build and start the Docker containers using the production environment file:

   ```bash
   docker-compose --env-file .env.production up --build -d
   ```

   The `-d` flag runs the containers in detached mode.

### Stopping the Containers

To stop the running containers:

```bash
docker-compose down
```

This command stops and removes the containers. The database data is stored in a Docker volume and is retained even after the containers are removed.

## Database Migrations

Once the containers are up, you’ll need to apply Django migrations:

```bash
docker-compose exec web python manage.py migrate
```

## Creating a Superuser

To create a Django superuser, run:

```bash
docker-compose exec web python manage.py createsuperuser
```

## Accessing the Django Shell

You can access the Django shell within the running container using:

```bash
docker-compose exec web python manage.py shell
```

## Troubleshooting

### ProgrammingError: relation 'django_site' does not exist

If you encounter the error **"ProgrammingError at /accounts/login/ relation 'django_site' does not exist,"** follow these steps to resolve it:

1. **Ensure the Sites Framework is Installed:**
   Make sure the Django Sites framework is included in your `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       'django.contrib.sites',
       ...
   ]
   ```

2. **Run Migrations:**
   After confirming that the Sites framework is installed, run the migrations to create the necessary database tables:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Check the DATABASES Setting:**
   Ensure your `DATABASES` setting in `settings.py` is correctly configured.

4. **Creating a Site:**
   If you haven’t already, create a site entry using the Django shell:

   ```bash
   docker-compose exec web python manage.py shell
   ```

   Then run:

   ```python
   from django.contrib.sites.models import Site
   Site.objects.create(domain='localhost:8000', name='My Site')
   ```

5. **Check for Migration Conflicts:**
   To verify applied migrations, run:

   ```bash
   docker-compose exec web python manage.py showmigrations
   ```

### General Troubleshooting

- **Database Connection Issues**: Ensure your `.env` files are correctly configured and that `db` is the `DATABASE_HOST` in both `.env.local` and `.env.production`.
- **Port Conflicts**: Make sure port `8000` is not in use by another service.

## Cleaning Up

To remove all containers, networks, and volumes:

```bash
docker-compose down -v
```

This command stops and removes containers, networks, and volumes, including the database data.

---

This `README.md` should help new team members and other contributors set up and work on the project. For further assistance, feel free to reach out to the team.
```

### Key Additions:
- A new section on **ProgrammingError** has been added under **Troubleshooting**, detailing steps to resolve the issue related to the missing `django_site` table.
- Clear instructions have been included to assist users in troubleshooting this specific error effectively. 

Feel free to adjust any specific wording or details as needed!