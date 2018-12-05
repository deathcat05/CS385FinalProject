#DOCKERFILE

FROM python:2.7
#Allows us to create environment variables for django application
ENV PYTHONBUFFERED 1 
#OS Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip install -U pip setuptools

RUN mkdir django_app

WORKDIR django_app

COPY requirements.txt /django_app/

RUN pip instiall requirements.txt

ADD . /django_app/ 

EXPOSE 8888

CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]