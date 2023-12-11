FROM php:8.1-apache

# Set working directory
WORKDIR /var/www/html

# Install dependencies
RUN apt-get update && apt-get install -y \
    libzip-dev \
    unzip \
    wget \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    && docker-php-ext-install zip

# Download and install Python 3.10.12
RUN wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tar.xz && \
    tar -xf Python-3.10.12.tar.xz && \
    cd Python-3.10.12 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf Python-3.10.12 Python-3.10.12.tar.xz

# Set working directory
WORKDIR /var/www/html

# Create and activate a virtual environment
RUN python3.10 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# 必要なライブラリをインストール
RUN apt-get install -y libx11-dev
RUN apt-get install -y libgl1-mesa-glx
RUN pip install open3d 
RUN apt-get install -y libglib2.0-0
RUN pip install opencv-python
RUN pip install torch


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
