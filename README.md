# CS385 Instagram clone

### To get everything started at once
source install.sh

##### To import dependencies into your virtualenv  
source venv/bin/activate  #activate venv  
pip install -r requirements.txt

or run ./install.sh  
after running make sure to start your virtualenv.

##### To run server
./runserver.sh

#### If you delete your venv file on accident
virtualenv venv # to create the file
./install.sh

#### Your venv file must be in the same directory as your install.sh





#########################
#   FOR CABERA TO USE   #
#########################

1) Create a VM instance on google cloud:
    gcloud compute instances create instagram-clone --zone=us-west1-c --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server --image=ubuntu-1804-bionic-v20180823 --image-project=ubuntu-os-cloud --boot-disk-size=20GB --boot-disk-type=pd-standard --boot-disk-device-name=instagram-clone

2) Install necessary VM requirements:
    make requirements


3) Build the docker image
    make build 



