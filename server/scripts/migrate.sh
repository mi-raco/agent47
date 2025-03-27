#!/bin/bash

# Run database migrations
docker-compose run app alembic upgrade head