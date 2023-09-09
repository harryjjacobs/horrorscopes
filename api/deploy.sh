#!/bin/bash

export GOOGLE_CLOUD_PROJECT=$@

gcloud config unset project
gcloud config set project ${GOOGLE_CLOUD_PROJECT}

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/horrorscope-api

# Deploy to Cloud Run
gcloud run deploy horrorscope-api --image gcr.io/${GOOGLE_CLOUD_PROJECT}/horrorscope-api --region europe-west2
