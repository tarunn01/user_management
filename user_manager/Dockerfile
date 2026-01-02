# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libexpat1 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file into the container
COPY .env .

# Copy the rest of the application code
COPY . .

# Run the application directly
# CMD ["/usr/local/bin/uwsgi", "--ini", "uwsgi.ini"]

 #TEMPORARY: Run the Flask development server to get a better error message.
 #We will change this back to the uwsgi command later.
 CMD ["python", "app.py"]