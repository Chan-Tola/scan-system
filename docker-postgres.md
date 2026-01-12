Connection & Basic Info

# Connect to PostgreSQL (interactive shell - if supported)
docker exec -it postgres_db psql -U useradmin -d attendance_db

# Show 
SELECT id, username, email FROM users ORDER BY id;

# Delete 
DELETE FROM users WHERE id = 22;

# Table Operations
# List all tables
docker exec -it postgres_db psql -U useradmin -d attendance_db -c "\dt"

#Check Table Columns + relationship
docker exec -it postgres_db psql -U useradmin -d attendance_db -c "\d table_name"
# example docker exec -it postgres_db psql -U useradmin -d attendance_db -c "\d users"

Select All Data from a Table
# exmplae  docker exec -it postgres_db psql -U useradmin -d attendance_db -c "SELECT * FROM attendances;" 
docker exec -it postgres_db psql -U useradmin -d attendance_db -c "SELECT * FROM attendances;"



DELETE FROM attendances WHERE id = 7;

docker exec -it postgres_db psql -U useradmin -d attendance_db -c "SELECT * FROM attendances;"
