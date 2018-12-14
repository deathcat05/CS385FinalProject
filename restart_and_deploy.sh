#!/bin/bash

kubectl delete deployment instaclone ; \
kubectl delete service instaclone ; \
docker build -t gcr.io/rare-decker-110703/instaclone . ; \
gcloud docker -- push gcr.io/rare-decker-110703/instaclone ; \
kubectl create -f kubernetes.yaml
