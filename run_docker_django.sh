#! /bin/bash

docker build . -t hello && \
docker run -p 8000:8000 hello

