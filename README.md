# CS385 Instagram clone

## To get everything started at once
`source install.sh`

## Authentication
The key you are returned from `/account/register` and `/account/login` is your Authorization Token<br>
Insert it into your header as:<br>
`Authorization:Token 48c2e4754bc3d765c1cc611681f5b7492bec1f73`<br>

## Endpoints
`POST /account/register`<br>
`POST /account/login`<br>
`POST /account/logout`<br>
`POST /content`

## To import dependencies into your virtualenv  
`source venv/bin/activate  #activate venv && pip install -r requirements.txt`<br>
<b>Your venv file must be in the project root directory `~CS385FinalProject`</b><br><br>
or alternatively, run `source install.sh`<br>

## To run server
`./runserver.sh`
