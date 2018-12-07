all: requirements build

build: requirements
	docker-compose run web django-admin.py startproject InstagramClone
	
requirements: 
	./requirements.sh

