# stop all the container 
docker-compose stop 
# start all the container
# docker-compose start
# Restart all the contain
# docker-compose restart 

# docker-compose up -d : Start everything. The -d (detached) keeps your terminal free so you can keep working while the containers run in the background.
# docker-compose down : Clean stop. Unlike stop, this removes the containers and networks completely. Use this if you are experiencing "weird" network errors.


# docker compose build ( name image ) 
# exmaple
docker compose build api-scan
# What it does:
# 1. Looks at docker-compose.yml
# 2. Finds "api-scan" service section
# 3. Builds Docker image using Dockerfile
# 4. ✅ Image is ready but container NOT running yet

# docker compose up -d ( name image )
# example
docker compose up -d api-scan
# What it does:
# 1. Checks if image exists
# 2. If not, builds it automatically
# 3. Creates and starts the container
# 4. Runs it in background (-d = detached)
# 5. ✅ Container is NOW running

# Rebuild and Restart
# Run this command in your terminal to force Docker to rebuild the gateway with the new folder structure:

# up build again for specific folder
# docker-compose up --build -d ( name image )
# example docker-compose up --build -d api-gateway

# check the log if not have docker-desktop
docker-compose logs -f ( name image )
# example docker logs api-gateway



docker logs api-staff-management --tail 50

docker-compose up --build -d api-staff-management


