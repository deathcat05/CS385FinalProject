# Instagram Clone
## CDN: AWS S3
## Runs on Kubernetes, in which each pod is a combination of Django and SQL Proxy
## Database: MySQL with master/slave 

    
# Steps for running application
<b>If you have any troubles with these initial instructions please refer to instruction set 2 located at the bottom of this README. Also please feel free to email any of us.

joemissamore@live.com
</b>


## Database
- Create a MySQL (2nd generation instance on Google Cloud) instance
- Create a Database
- Create a user
- Make sure the Cloud SQL API is enabled for your project

### Permissions
- You will need to make sure you permissions are set with IAM & admin.
  - Select 'Service accounts' on the left and click on your project
  - Click 'edit' and create a key
  - <b>This needs to be downloaded as .json and put onto your VM instance</b>

## Create a new VM instance on Google Cloud 

	 gcloud compute instances create instagramclone --zone=us-west1-c --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server --image=ubuntu-1804-bionic-v20180823 --image-project=ubuntu-os-cloud --boot-disk-size=20GB --boot-disk-type=pd-standard --boot-disk-device-name=instagramclone

## Install update VM & Install Docker
  
   	sudo ./init_server.sh

## Logout and re-login to VM Instance to allow for Docker to be utilized 

## Create an AWS S3 Bucket
You will need to acquire and access key and a secret key.

# Prepare the app
Fill in these variables located inside the `./run.sh` file. 

    export PROJECT_ID=<YOUR_PROJECT_ID>
    export ZONE=<ZONE_FOR_CLUSTER>
    export DB_INSTANCE_NAME=<DB_INSTANCE_NAME>
    KEY_FILE=<KEY_FILE_GENERATED_FROM_IAM_SETTINGS>
    CLUSTER_NAME=<YOUR_DESIRED_CLUSTER_NAME>

    export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_KEY>
    export AWS_ACCESS_KEY=<AWS_ACCESS_KEY>
    export DATABASE_USER=<DB_USERNAME>
    export DATABASE_PASSWORD=<DB_PASSWORD>

The `KEY_FILE` is the key that was generated with IAM & admin, the step located under permissions.

# Run the app
`source ./run.sh`


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


# Instruction Set 2
Getting things started
1) Create a VM instance by entering the command below
in the GCP active cloud shell:

        gcloud compute instances create instaclone \
        --zone=us-west1-c --machine-type=n1-standard-1 \
        --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE \
        --scopes=https://www.googleapis.com/auth/cloud-platform \
        --tags=http-server,https-server --image=ubuntu-1804-bionic-v20180823 \
        --image-project=ubuntu-os-cloud --boot-disk-size=20GB \
        --boot-disk-type=pd-standard --boot-disk-device-name=instaclone


2) Ensuring that you google cloud engine is communicating with SQL 
and other APIs

- Go to APIs & Services
- Click on Enable APIs & Services
- Search Kubernetes Engine API - enable it
- Search Cloud SQL - enable it


3) Pull down project
- git clone https://github.com/deathcat05/CS385FinalProject.git

-----------------------------------------------------------------------

Setting up SQL on google cloud console
1) Left navigation bar
2) Go down to SQL
3) Create instance
4) Choose MySQL
5) Choose Second Generation
6) Fill out instance id and set root password
7) Next in the GCP side panel, go to IAM & admin and select Service accounts
8) Click on your service account
9) CLick edit at the top
9) At the bottom, click create key and select json and hit create
10) A new file will download.
11) cd into the project file pulled down from github and add this file
into the CS385FinalProject directory or create a file named the same as
the downloaded json file and make sure to copy and paste the content 
into it and save it as a .json.
12) Go back to SQL tab in GCP
13) Click on your database
14) Click Create user account
15) username set to instaclone
16) password set to instaclone
17) allow any host
18) Click create
19) Go to your VPC network tab
20) Click external ip addresses
21) In the In use by column, find your instance's name
22) In the Type column, make sure your instance's external 
IP address is static
- If it's ephemeral, then click and reserve a new static Address
23) If you give it a static ip, name it instaclone and give a description
24) Write down that static IP, you will need it later 
25) Open the navigation menu. Under Storage, click SQL
26) Click the name of the SQL instance that you want to connect
27) Click the Connections tab
28) Click Add network
29) Enter the static IP address of your VM instance
30) Click Done and Save
31) In the Connect to this instance card, copy or write down the IP address listed
32) Go to your compute engine and find your vm instance
33) ssh into your instance
34) sudo apt-get update
35) sudo apt-get install mysql-client
- Enter y for all
36) Enter the following and replace [INSTANCE_IP_ADDR] with the IP address of your own Cloud SQL instance:
- mysql --host=[INSTANCE_IP_ADDR] \
    --user=root --password


-----------------------------------------------------------------------

Log into your google cloud instance 
- touch setup_docker.sh
- chmod +x setup_docker.sh
- Add these commands into the file

#!/bin/bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce=18.06.1~ce~3-0~ubuntu
sudo usermod -aG docker $USER

3) ./init_server

4) Update current environment variables by running this command:

echo $'AWS_SECRET_ACCESS_KEY=<KEY>\n
AWS_ACCESS_KEY=<KEY>\n
DATABASE_USER=<DB_USER>\n
DATABASE_PASSWORD=<DB_PASS>\n' | sudo tee --append /etc/environment

1) restart shell to update commands that were set in setup_docker.sh and
set_env.sh

6) cd into CS385FinalProject

7) install kubernetes
- sudo snap install kubectl --classic

8) create kubernetes cluster
- gcloud container clusters create djangocluster --zone us-west1-c

9) gcloud auth configure-docker

10) create cloud sql oath
- kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.json=<name of json file created from SQL key>

11) create secret for sql password
- kubectl create secret generic cloudsql --from-literal=username=$DATABASE_USER --from-literal=password=$DATABASE_PASSWORD

12) create secret for aws
- kubectl create secret generic aws --from-literal=accesskey=$AWS_ACCESS_KEY --from-literal=secretkey=$AWS_SECRET_ACCESS_KEY

13) activate service account
- gcloud auth activate-service-account --key-file=<name of json file created from SQL key>

14) Edit the kubernetes.yaml file and replace places with PROJECT_ID with you project id. 

15) docker build -t gcr.io/<PROJECT_ID>/instaclone .

16) gcloud docker -- push gcr.io/<PROJECT_ID>/instaclone

17) kubectl create -f kubernetes.yaml
- watch -n 2 kubectl get services
- wait for external ip address to appear
- once it is populated, you can post it into your browser and connect
- refer to readme on github to use endpoints and test
