Connection & Basic Info

# Connect to PostgreSQL (interactive shell - if supported)
docker exec -it postgres_db psql -U useradmin -d attendance_db

# Table Operations
# List all tables
docker exec -it postgres_db psql -U useradmin -d attendance_db -c "\dt"

#Check Table Columns + relationship
docker exec attendance_postgres psql -U admindbps -d attendance_db -c "\d table_name"
# example docker exec attendance_postgres psql -U admindbps -d attendance_db -c "\d users"







