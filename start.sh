#!/usr/bin/env bash

# Get the directory path of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the path to your .env file and Docker compose file relative to the script directory
ENV_FILE=".env"
DOCKER_COMPOSE_FILE="docker-compose-file.yml"

# Construct the full path to the Docker Compose file
FULL_ENV_PATH="$SCRIPT_DIR/$ENV_FILE"
FULL_DOCKER_COMPOSE_PATH="$SCRIPT_DIR/$DOCKER_COMPOSE_FILE"

# Check if the .env file exists
if [ ! -f "$FULL_ENV_PATH" ]; then
  echo ".env file not found: $FULL_ENV_PATH"
  exit 1
fi

# Load the environment variables
source "$FULL_ENV_PATH"

# Check if the Docker Compose file exists
if [ ! -f "$FULL_DOCKER_COMPOSE_PATH" ]; then
  echo "Docker Compose file not found: $FULL_DOCKER_COMPOSE_PATH"
  exit 1
fi

# Check if the specific containers are running. If so, tear them down.
if docker-compose -f "$FULL_DOCKER_COMPOSE_PATH" ps -q; then
  echo "Existing containers found. Tearing them down..."
  docker-compose -f "$FULL_DOCKER_COMPOSE_PATH" down
fi

# Run docker-compose up
docker-compose -f "$FULL_DOCKER_COMPOSE_PATH" up
