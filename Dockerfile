FROM python:3.10.13

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install gettext for managing translations
RUN apt-get update && apt-get install -y gettext

# Install psycopg2 dependencies
RUN apt-get install -y libpq-dev

# Install pip
RUN python -m pip install --upgrade pip

# Install application dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

RUN apt-get install -y google-chrome-stable


    && unzip -q /usr/local/bin/chromedriver_linux64.zip -d /usr/local/bin \
    && rm /usr/local/bin/chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

# Copy the application files into the image
COPY . /app/

# Expose port 8000 on the container
EXPOSE 8000