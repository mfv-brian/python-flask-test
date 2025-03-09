# Infrastructure Setup

This directory contains Docker configurations for running the application's infrastructure dependencies.

## MySQL Database

A containerized MySQL 8.0 database is provided for local development.

### Usage

Start the MySQL container:

```bash
cd infra
docker-compose up -d
```

Stop the container:

```bash
cd infra
docker-compose down
```

### Connection Details

- **Host**: localhost
- **Port**: 3307
- **Database**: app_db
- **Username**: app_user
- **Password**: app_password
- **Root Password**: root_password

### Persistence

Data is persisted in a Docker volume named `mysql_data`. To completely reset the database, you need to remove this volume:

```bash
docker-compose down -v
```

## Database Migrations

The database uses a simple migration system to version control the schema. Migrations are automatically applied when the container starts.

### How it works

1. Migration files are stored in the `migrations/` directory.
2. Files follow the naming convention: `V{number}__{description}.sql` (e.g., `V1__initial_schema.sql`).
3. The `migrate.sh` script applies migrations in numerical order.
4. Each migration is applied only once, tracked in the `migrations` table.

### Adding a new migration

To add a new migration:

1. Create a new SQL file in the `migrations/` directory following the naming convention.
2. Restart the MySQL container:

```bash
cd infra
docker-compose restart
```

Or to see the migration logs:

```bash
cd infra
docker-compose down
docker-compose up
``` 