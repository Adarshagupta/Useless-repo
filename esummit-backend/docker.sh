#!/bin/bash

# Make this script executable with: chmod +x docker.sh

case "$1" in
  build)
    docker-compose build
    ;;
  up)
    docker-compose up -d
    ;;
  down)
    docker-compose down
    ;;
  logs)
    docker-compose logs -f
    ;;
  shell)
    docker-compose exec web bash
    ;;
  db)
    docker-compose exec db psql -U postgres -d esummit
    ;;
  migrate)
    docker-compose exec web flask db upgrade
    ;;
  create-admin)
    docker-compose exec web python create_admin.py
    ;;
  restart)
    docker-compose restart
    ;;
  *)
    echo "Usage: $0 {build|up|down|logs|shell|db|migrate|create-admin|restart}"
    echo ""
    echo "build       - Build the Docker images"
    echo "up          - Start the containers in the background"
    echo "down        - Stop and remove the containers"
    echo "logs        - Follow the logs"
    echo "shell       - Get a shell in the web container"
    echo "db          - Get a PostgreSQL shell"
    echo "migrate     - Run database migrations"
    echo "create-admin- Create an admin user"
    echo "restart     - Restart all services"
    exit 1
esac 