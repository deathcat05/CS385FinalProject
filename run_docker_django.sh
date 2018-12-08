#! /bin/bash

docker build . -t hello && \
docker run -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY -p 8000:8000 hello

