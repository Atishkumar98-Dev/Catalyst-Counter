## Project Structure

```
.
├── app/                          # Django project files
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── .env.local                    # Local development environment variables
├── .env.production               # Production environment variables
```

## Environment Variables

### Local Development

Create a `.env.local` file with the following variables:

```env
DEBUG=True
DATABASE_NAME=your_local_db_name
DATABASE_USER=your_local_db_user
DATABASE_PASSWORD=your_local_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

### Production

Create a `.env.production` file with your production settings:

```env
DEBUG=False
DATABASE_NAME=your_production_db_name
DATABASE_USER=your_production_db_user
DATABASE_PASSWORD=your_production_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

## Running the Project

### Local Development

1. Create and configure `.env.local`.
2. Build and start the Docker containers:

   ```bash
   docker-compose --env-file .env.local up --build
   ```

   Access the app at `http://localhost:8000`.

### Production

1. Create and configure `.env.production`.
2. Build and start the Docker containers:

   ```bash
   docker-compose --env-file .env.production up --build -d
   ```

   Use the `-d` flag to run in detached mode.

## Stopping the Containers

To stop the running containers, run:

```bash
docker-compose down
```

## Database Migrations

Apply migrations with:

```bash
docker-compose exec web python manage.py migrate
```

## Creating a Superuser

Create a Django superuser with:

```bash
docker-compose exec web python manage.py createsuperuser
```

## Troubleshooting

### Common Issues

- **Database Connection Issues**: Check your `.env` files for correct configuration.
- **Port Conflicts**: Ensure port `8000` is not in use by another service.

---
