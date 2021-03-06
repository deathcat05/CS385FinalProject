# start from an official image
FROM python:2.7

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# install our two dependencies
RUN pip install gunicorn

# copy our project code
COPY . /opt/services/djangoapp/src

RUN pip install -r requirements.txt

# expose the port 8080
EXPOSE 8080

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "django_app", "--bind", ":8080", "instagram_clone.wsgi:application"]
