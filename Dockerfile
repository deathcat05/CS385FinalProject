#DOCKERFILE
FROM python:2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /InstagramClone
 WORKDIR /InstagramClone
 ADD requirements.txt /InstagramClone/
 RUN pip install -r requirements.txt
 ADD . /InstagramClone/