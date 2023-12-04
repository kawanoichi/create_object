FROM php:8.1-apache

# Set working directory
WORKDIR /var/www/html

# Install dependencies
RUN apt-get update && apt-get install -y \
    libzip-dev \
    unzip \
    && docker-php-ext-install zip

# Install Python
RUN apt install -y python3

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

COPY create_object /var/www/html

# Apacheの設定ファイルをコピー
COPY apache-config.conf /etc/apache2/sites-available/000-default.conf

RUN a2enmod rewrite

# Expose port 9000 and start php-fpm server
EXPOSE 80

# CMD ["php-fpm"]
CMD ["apache2-foreground"]
