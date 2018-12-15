## Docker 
The Django application in this directory should be ignored, it's only for testing.

# Before running the application, the following components need to be active: 
    - Google Cloud SQL Instance Setup
        - Name: instaclone
        - Password: <create a password>
    
    - In `kubernetes.yaml`, replace <YOUR_PROJECT_ID> with you Google Cloud Project ID 

    
# Steps for running application

## Create a new VM instance on Google Cloud 

	 gcloud compute instances create instagramclone --zone=us-west1-c --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server --image=ubuntu-1804-bionic-v20180823 --image-project=ubuntu-os-cloud --boot-disk-size=20GB --boot-disk-type=pd-standard --boot-disk-device-name=instagramclone

## Install update VM & Install Docker
  
   	sudo ./init_server.sh

## Logout and re-login to VM Instance 

## Install & Create kubernetes cluster

    	sudo snap install kubectl --classic

	  gcloud container clusters create djangocluster --zone us-west1-c

## Create Cloud SQL Oath
### Here, be sure to replace `<YOUR_JSON_CRED_FILE>` with the .json file from SQL Cloud

    kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.<YOUR_JSON_CRED_FILE>

## Create Secret for SQL Password

    kubectl create secret generic cloudsql --from-literal=username=$DATABASE_USER --from-literal=password=$DATABASE_PASSWORD

## Create secret for AWS

    kubectl create secret generic aws --from-literal=accesskey=$AWS_ACCESS_KEY --from-literal=secretkey=$AWS_SECRET_ACCESS_KEY

## Create Google Cloud Service Account 
### Here, be sure to replace `<YOUR_JSON_CRED_FILE>` with the .json file from SQL Cloud

  	gcloud auth activate-service-account --key-file=<YOUR_JSON_CRED_FILE>

## Clone project repository
  
    git clone https://github.com/deathcat05/CS385FinalProject.git
    cd CS385FinalProject
 
## Configure Docker Authorization

	gcloud auth configure-docker

## Build Docker Image
   
    Here, replace `<PROJECT_ID>`, with your Google Cloud Project ID 

    docker build -t gcr.io/<PROJECT_ID>/instaclone .

## Push Docker Image
### Here, replace `<PROJECT_ID>`, with your Google Cloud Project ID 
   	
	gcloud docker -- push gcr.io/<PROJECT_ID>/instaclone

## Create Kubernetes Pods

    kubectl create -f kubernetes.yaml

# Authentication
The key you are returned from `/account/register` and `/account/login` is your Authorization Token<br>
Insert it into your header as: <br>`Authorization:Token <token>`<br>

# Endpoints 

### POST /account/register/ 
Used to register an account.

	curl -X POST -H 'Content-Type: application/json' http://35.203.173.140/account/register/ -d '{"username": "<user_name>", "email": "<email>", "password1": "<password>", "password2": "<password>"}'
	

### POST /account/token/ 
Use to login an establish a session

	curl -X POST -H 'Content-Type: application/json' http://35.203.173.140/account/login/ -d '{"username": "<username>", "email": "<email>", "password": "<password>"}'

### DELETE /account/token/ 
Used to delete/deactivate a token. 

	curl -X DELETE -H 'Authorization: Token <token provided when creating account>' http://35.203.173.140/content/<id of post>/

### POST /content/
Allows a multipart file upload. This endpoint also allows including comments and tags. This endpoint requires an active authenticated user, which will become the owner of the content. Returns the id of the content that was added. Since the content needs to be processed, you might not be able to return the URL of the renditions on the response, case in which you should return the appropriate corresponding status code. 

Command: Used within Postman 

To use `POST /content` endpoints enter the following into postman:

- Values are represented as `<key>:<value>`
- <b>This must be used as `multipart/form-data`</b>
  - Header
    - `Content-Type:multipart/form-data`
    - `Authorization:Token <token>`
  - Body
    - `original_image: /path/to/your/jpg`
    - `tag:tag1`
    - `tag:tag2`
    - `tag:tagN` (last tag)
      - You can have as many tags as you want
    - `description:A description`
>>>>>>> da3f87741b8b22162e68e8094e936bfe40d611ba

## Authentication
Uses token bases authentication<br>
The key or token you are returned from `/account/register` and `/account/login` is your Authorization Token<br>
Insert it into your header as:<br>
`Authorization:Token <token>`<br>

## Endpoints
`POST /account/register`<br>
`POST /account/login`<br>
`POST /account/logout`<br>
`POST /content`
`PUT /content`
- To use `PUT /content` or `POST /content` endpoints enter the following into postman
- Values are represented as `<key>:<value>`
- <b>This must be used as `multipart/form-data`</b>
  - Header
    - `Content-Type:multipart/form-data`
    - `Authorization:Token <token>`
  - Body
    - `original_image: /path/to/your/jpg`
    - `tag:tag1`
    - `tag:tag2`
    - `tag:tagN` (last tag)
      - You can have as many tags as you want
    - `description:A description`

## To restart and run Kubernetes
`./restart_kubes.sh`

## To restart and deploy Kubernetes
`./restart_and_deploy.sh`

## To import dependencies into your virtualenv  
`source venv/bin/activate  #activate venv && pip install -r requirements.txt`<br>
<b>Your venv file must be in the project root directory `~/CS385FinalProject/`</b><br><br>
or alternatively, run `source install.sh`<br>

## To run server Django only
`./runserver.sh`
