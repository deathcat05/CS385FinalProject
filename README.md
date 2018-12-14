README.md

## Create VM Instance on GCloud Platform with command: 
	gcloud compute instances create instaclone --zone=us-west1-c --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server --image=ubuntu-1804-bionic-v20180823 --image-project=ubuntu-os-cloud --boot-disk-size=20GB --boot-disk-type=pd-standard --boot-disk-device-name=instaclone

## Run the following script 

## The following endpoints can be used to interact with the applicaton: 

### POST /account/register 
Used to register an account.

	curl -X POST -H 'Content-Type: application/json' http://35.203.173.140/account/register/ -d '{"username": "<user_name>", "email": "<email>", "password1": "mypassword", "<password>": "<password>"}'

### POST /account/token 
Use to login an establish a session

	curl -X POST -H 'Content-Type: application/json' http://35.203.173.140/account/login/ -d '{"username": "<username>", "email": "<email>", "password": "<password>"}'

### DELETE /account/token 
Used to delete/deactivate a token. 

	curl -X DELETE -H 'Authorization: Token <token provided when creating account>' http://35.203.173.140/content/<id of post>/

### POST /content 
Allows a multipart file upload. This endpoint also allows including comments and tags. This endpoint requires an active authenticated user, which will become the owner of the content. Returns the id of the content that was added. Since the content needs to be processed, you might not be able to return the URL of the renditions on the response, case in which you should return the appropriate corresponding status code. 

Command: Demo in class

To use POST /content endpoints enter the following into postman:

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
Command: Demo in class
To use PUT /content endpoints enter the following into postman:
Values are represented as <key>:<value>

This must be used as multipart/form-data
Header
Content-Type:multipart/form-data
Authorization:Token <token>
Body
original_image: /path/to/your/jpg
tag:tag1
tag:tag2
tag:tagN (last tag)
You can have as many tags as you want
description:A description

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







### GET /feed 
Returns the feed for the currently logged in user. 

	curl -X GET -H "Authorization: Token <token>" http://35.203.173.140/feed/

### POST /search 
Returns a list of content whose tags or description match a search query. The search query consists of a single string.

	curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <token>" -d '{"search": "<search_string>"}' http://35.203.173.140/search/


