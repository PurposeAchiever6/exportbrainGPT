# Function to run SQL file
run_sql_file() {
    local file="$1"
    PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" -f "$file"
}

# Flag to indicate whether to prompt for DB info
prompt_for_db_info=false

# Check if .migration_info exists and source it
if [ -f .migration_info ]; then
    source .migration_info
    # Check if any of the variables are empty
    if [ -z "$DB_HOST" ] || [ -z "$DB_NAME" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
        prompt_for_db_info=true # Some values are empty, so prompt user for values
    fi
else
    prompt_for_db_info=true # No .migration_info file, so prompt user for values
fi

run_sql_file "scripts/init_tables.sql"