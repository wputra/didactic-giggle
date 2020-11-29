#!/bin/bash
TAG=$(git rev-parse --short HEAD)
docker build -t wputra/flasktest:$TAG .
docker tag wputra/flasktest:$TAG wputra/flasktest:latest

docker-compose up -d
