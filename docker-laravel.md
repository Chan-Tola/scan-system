Initialize Laravel (Inside Container)

docker exec -it api-staff-management php artisan 

# Generate App Key
docker exec -it api-staff-management php artisan key:generate
    
# Finalize Octane binary inside Linux
docker exec -it api-staff-management php artisan octane:install --server=frankenphp


# rollback
docker-compose exec api-staff-management php artisan migrate:rollback


# Run migrations (including Spatie tables)
migrate          migrate table to DB

# PHP comand
docker exec -it api-staff-management php artisan make

make:command:    Create a new Artisan command
make:seeder:     Create a new seeder class
make:controller: Create a new controller class
make:request:    Create a new form request class
docker-compose exec api-staff-management php artisan optimize:clear




  