#! /bin/bash

docker build . -t django_app_docker && \
docker run -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY -p 8000:8000 django_app_docker

