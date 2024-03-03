FROM python:3.11.7

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install psycopg2 dependencies
RUN apt-get update && apt-get install -y libpq-dev

# Install pip
RUN python -m pip install --upgrade pip

# Install application dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application files into the image
COPY . /app/

# Expose port 8000 on the container
EXPOSE 8000