VM-update: 
	sudo /scripts/init_server.sh

kubectl-build: 
	sudo snap install kubectl --classic
	gcloud container clusters create djangocluster --zone us-west1-c

generate-secrets:
	kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.<YOUR_JSON_CRED_FILE>
	kubectl create secret generic cloudsql --from-literal=username=$DATABASE_USER --from-literal=password=$DATABASE_PASSWORD
	kubectl create secret generic aws --from-literal=accesskey=$AWS_ACCESS_KEY --from-literal=secretkey=$AWS_SECRET_ACCESS_KEY

create-service_account: 
	gcloud auth activate-service-account --key-file=rare-decker-110703-118d6761a9c0.json

git-init:
	git clone https://github.com/deathcat05/CS385FinalProject.git
	cd CS385FinalProject