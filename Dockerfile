FROM php:8.1-apache

# Set working directory
WORKDIR /var/www/html

# Install dependencies
RUN apt-get update && apt-get install -y \
    libzip-dev \
    unzip \
    && docker-php-ext-install zip

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

COPY create_object /var/www/html

# Apacheの設定ファイルをコピー
COPY apache-config.conf /etc/apache2/sites-available/000-default.conf

RUN a2enmod rewrite

# Expose port 9000 and start php-fpm server
EXPOSE 80

# pyenvのためにgitをインストール
RUN apt -y install git

# pyenv
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl

RUN curl https://pyenv.run | bash && \
    echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Reload the shell
SHELL ["/bin/bash", "--login", "-c"]

RUN pyenv install 3.10 && \
    pyenv global 3.10 && \
    python3 -m venv /venv

# Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc

# opencv関連のファイルを追加
RUN apt-get install -y libgl1-mesa-glx
RUN echo export LD_LIBRARY_PATH=/path/to/directory/containing/libGL.so.1:$LD_LIBRARY_PATH >> ~/.bashrc
RUN apt-get install -y libglib2.0-0

# Reload the shell
SHELL ["/bin/bash", "--login", "-c"]

# CMD ["php-fpm"] 一番下に追記
CMD ["apache2-foreground"]
