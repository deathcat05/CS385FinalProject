#!/bin/bash

kubectl delete deployment instaclone ; \
kubectl delete service instaclone ; \
kubectl create -f kubernetes.yaml;
