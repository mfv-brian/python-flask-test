#!/bin/bash
set -e

# Database connection parameters
DB_HOST="localhost"
DB_PORT="3307"
DB_USER="app_user"
DB_PASS="app_password"
DB_NAME="app_db"

echo "Running MySQL migrations..."

# Find all migration scripts and sort them
migrations=$(find /docker-entrypoint-initdb.d/migrations -name "V*__*.sql" | sort)

for migration in $migrations; do
  # Extract version number from filename (e.g., V1__description.sql -> 1)
  version=$(basename "$migration" | sed -E 's/V([0-9]+)__.*/\1/')
  
  echo "Checking migration version $version: $migration"
  
  # Check if this migration has already been applied
  already_applied=$(mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASS $DB_NAME -N -e \
    "SELECT COUNT(*) FROM migrations WHERE version = $version;" 2>/dev/null || echo "0")
  
  # If migrations table doesn't exist yet, create it and set already_applied to 0
  if [ $? -ne 0 ]; then
    echo "Creating migrations table..."
    mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASS $DB_NAME -e \
      "CREATE TABLE IF NOT EXISTS migrations (version INT PRIMARY KEY, applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    already_applied=0
  fi
  
  # Apply migration if not already applied
  if [ "$already_applied" -eq "0" ]; then
    echo "Applying migration $version: $migration"
    mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASS $DB_NAME < "$migration"
    
    # Record that we applied this migration
    mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASS $DB_NAME -e \
      "INSERT INTO migrations (version) VALUES ($version);"
    
    echo "Migration $version applied successfully"
  else
    echo "Migration $version already applied, skipping"
  fi
done

echo "All migrations completed successfully" 