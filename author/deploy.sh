#!/bin/bash

export GOOGLE_CLOUD_PROJECT=$@

gcloud config unset project
gcloud config set project ${GOOGLE_CLOUD_PROJECT}

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/horrorscope-author

# Deploy to Cloud Run
gcloud run deploy horrorscope-author --image gcr.io/${GOOGLE_CLOUD_PROJECT}/horrorscope-author --update-secrets=/etc/secrets/openai-api-key=openai-api-key:latest --region europe-west2
