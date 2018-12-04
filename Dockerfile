#Dockerfile

FROM Python:2.7

ENV PYTHONBUFFERED 1

RUN mkdir /instagram-clone

WORKDIR /instagram-clone

COPY . /instagram-clone/

