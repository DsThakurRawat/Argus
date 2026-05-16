#!/bin/bash

# Copyright 2026 Divyansh Rawat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
PROJECT_ID="your-gcp-project-id" # Replace with your GCP Project ID
SERVICE_NAME="gemini-sre-agent"
REGION="us-central1" # Choose your desired GCP region
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# --- Build Docker Image ---
echo "Building Docker image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" .

# --- Push Docker Image to Google Container Registry ---
echo "Pushing Docker image to GCR..."
docker push "${IMAGE_NAME}"

# --- Deploy to Google Cloud Run ---
echo "Deploying to Google Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_NAME}" \
  --region "${REGION}" \
  --platform "managed" \
  --allow-unauthenticated \
  --project "${PROJECT_ID}" \
  --set-env-vars="GITHUB_TOKEN=${GITHUB_TOKEN}" \
  # Add other environment variables as needed, e.g., for specific service configs
  # --set-env-vars="SERVICE_CONFIG_PATH=/app/config/config.yaml" \
  # --update-secrets="GITHUB_TOKEN=GITHUB_TOKEN:latest" # Example for Secret Manager

echo "Deployment to Cloud Run complete!"
echo "Service URL: $(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --project ${PROJECT_ID} --format='value(status.url)')"