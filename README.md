## Docker 
The Django application in this directory should be ignored, it's only for testing.


## To get everything started at once
`source install.sh`

## Authentication
The key you are returned from `/account/register` and `/account/login` is your Authorization Token<br>
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

## To import dependencies into your virtualenv  
`source venv/bin/activate  #activate venv && pip install -r requirements.txt`<br>
<b>Your venv file must be in the project root directory `~/CS385FinalProject/`</b><br><br>
or alternatively, run `source install.sh`<br>

## To run server
`./runserver.sh`

## TODO
Talk about authentication<br>
Make tags one word?<br>
Dont allow users to access other endpoints<br>
