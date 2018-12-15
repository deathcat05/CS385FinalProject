# Instagram Clone
## CDN: AWS S3
## Runs on Kubernetes, in which each pod is a combination of Django and SQL Proxy
## Database: MySQL with master/slave 

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
  Here, be sure to replace `<YOUR_JSON_CRED_FILE>1 with the .json file from SQL Cloud

    kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.<YOUR_JSON_CRED_FILE>

## Create Secret for SQL Password

    kubectl create secret generic cloudsql --from-literal=username=$DATABASE_USER --from-literal=password=$DATABASE_PASSWORD

## Create secret for AWS

    kubectl create secret generic aws --from-literal=accesskey=$AWS_ACCESS_KEY --from-literal=secretkey=$AWS_SECRET_ACCESS_KEY

## Create Google Cloud Service Account 
  
  Here, be sure to replace `<YOUR_JSON_CRED_FILE>1 with the .json file from SQL Cloud

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
   Here, replace `<PROJECT_ID>`, with your Google Cloud Project ID 
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

### GET /content/{content id} 
Retrieves the URLs of the content, it’s owner, description and tags. It does not require authentication. Note that this service does not return the images itself, but the URLs where the different renditions of the content can be fetched. If the renditions are not ready, then a 202 status code should be returned.

	curl -X GET -H 'Content-Type: application/json' http://35.203.173.140/content/<content_id>/

### PUT /content/{content id} 
Allows replacing the description and tags of a specific piece of content. Only the owner of the content can perform this action 

Command: Used within Postman

To use `PUT /content` endpoints enter the following into postman:
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

Example of PUT or POST for /content on PostMan:



### DELETE /content/{content id}
 Deletes a piece content and its associated comments and tags. Only the owner of the content can perform this action 
 
	curl -X DELETE -H 'Authorization: Token <tokenx>' http://35.203.173.140/content/<content_id>/


### POST /subscriptions/ 
Subscribes an authenticated user to either another user or tags 

	curl -X POST \
	-H "Authorization: Token <your_token>" \
	-H "Content-Type: application/json" \
	-d '{"user": {"id": <user_id>} }' http://35.203.173.140/subscriptions/


### GET /subscriptions/ 
Returns the list of subscriptions for the current user. 

	curl -X GET -H "Authorization: Token <token>" http://35.203.173.140/subscriptions/



### GET /subscriptions/subscribers/{tag or username} 
Returns the list of subscribers to the current user 

User:

	curl -X GET -H "Authorization: Token <token>" http://35.203.173.140/subscriptions/subscribers/user/<user_id>/
Tag: 

	curl -X GET -H "Authorization: Token <token>" http://35.203.173.140/subscriptions/subscribers/tag/<tag_id>/

### GET /feed/
Returns the feed for the currently logged in user. 

	curl -X GET -H "Authorization: Token <token>" http://35.203.173.140/feed/

### POST /search/
Returns a list of content whose tags or description match a search query. The search query consists of a single string.

	curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <token>" -d '{"search": "<search_string>"}' http://35.203.173.140/search/



