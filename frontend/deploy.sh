#!/bin/bash

export GOOGLE_CLOUD_PROJECT=$@

gcloud config unset project
gcloud config set project ${GOOGLE_CLOUD_PROJECT}

npm run build

gcloud storage cp -R dist/* gs://horrorscope-frontend

gsutil -m setmeta -r -h "Cache-control: private, max-age 0" gs://horrorscope-frontend/index.html

# Useful bits from https://cloud.google.com/storage/docs/hosting-static-website
# make it public:
# gcloud storage buckets add-iam-policy-binding  gs://my-static-assets --member=allUsers --role=roles/storage.objectViewer
# add default index and 404 pages:
# gcloud storage buckets update gs://my-static-assets --web-main-page-suffix=index.html --web-error-page=404.html


# Note to future self: when trying to set up load balancer on google cloud storage
# and getting a vague error, make sure that Compute Engine API is enabled first 
# (discovered by opening browser console)