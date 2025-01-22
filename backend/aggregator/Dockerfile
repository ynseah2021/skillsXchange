# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    pkg-config \
    gcc \
    libpq-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /usr/local/bin/wait-for-it

RUN chmod +x /usr/local/bin/wait-for-it

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port for the Flask app
EXPOSE 5000

ENTRYPOINT ["wait-for-it", "db:3306", "--timeout=30", "--"]

# Run the Flask app
CMD ["python", "app.py"]