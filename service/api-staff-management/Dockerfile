FROM dunglas/frankenphp:1.2.4-php8.2-alpine

# Install system dependencies
RUN apk add --no-cache \
    git \
    unzip \
    libpq-dev \
    libzip-dev \
    bash \
    libjpeg-turbo-dev \
    libwebp-dev \
    freetype-dev \
    libpng-dev

# Install PHP extensions
RUN install-php-extensions pdo_pgsql pgsql gd intl zip opcache redis pcntl

WORKDIR /var/www/html

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copy application code
COPY . /var/www/html

# Set permissions
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

EXPOSE 80

ENV OCTANE_SERVER=frankenphp

# ✅ Use the FrankenPHP-specific Octane command
ENTRYPOINT ["php", "artisan", "octane:frankenphp", "--host=0.0.0.0", "--port=80", "--admin-port=2019"]
