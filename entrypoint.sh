#!/bin/bash

# Define cleanup function
cleanup() {
  echo "Running pre-stop hook..."
  python -m sync_databases save
}

# Trap SIGTERM (docker stop) and SIGINT (Ctrl+C)
trap cleanup SIGTERM SIGINT

# Start your main application
exec "$@" &

# Wait for the application to exit
wait $!