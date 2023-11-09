# Base image
FROM ubuntu:latest

# Set environment variables
ARG FLASK_PORT
ENV PORT=$FLASK_PORT

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nginx

# Set working directory
WORKDIR /app

# Copy the Flask application files to the container
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# Expose the Flask application port
EXPOSE $PORT

# Start the Flask application
CMD ["python3", "app.py"]
