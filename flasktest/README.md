# Overview
A URL shortening Flask micro website similar to bit.ly

# Requirement
- Docker (v19.03.12)
- Docker compose (v1.21.2)

# Deployment
- to start, do `docker-compose up -d`
- to deploy your changes, please execute `build-deploy.sh`

# TO DO
- Write explaination about system design: why you are going to implement like that.
- use redis as cache. the key is short_url, value is long_url
