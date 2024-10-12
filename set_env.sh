#!/bin/bash

# Check if the .env file exists
if [ ! -f .env ]; then
  echo ".env file not found!"
  exit 1
fi

# Export each variable from the .env file
export $(grep -v '^#' .env | xargs)
