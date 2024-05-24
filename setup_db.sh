#!/bin/bash

# This script automates the process of setting up a PostgreSQL database for this project to simplify
# the initial configuration for other developers or in deployment environments.
# It is for usage in Unix-based systems (Linux/macOS).
# The user will be granted all privileges on the newly created database.

# Exit on any error
set -e

echo "Creating PostgreSQL database and user..."

# Prompt for user, and password
read -p "Enter database user: " dbuser
read -sp "Enter database password: " dbpass
echo

# Create the database, user and grant all privileges to user
dbname="tresstime_db"
createdb $dbname
psql -d $dbname -c "CREATE USER $dbuser WITH ENCRYPTED PASSWORD '$dbpass';"
psql -d $dbname -c "GRANT ALL PRIVILEGES ON DATABASE $dbname TO $dbuser;"
psql -d $dbname -c "ALTER ROLE $dbuser CREATEDB"
echo "Database and user created successfully."
