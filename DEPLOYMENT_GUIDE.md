# 🚀 Complete Deployment Guide for Expense Tracker on GCP

This guide will walk you through deploying your Expense Tracker application to Google Cloud Platform (GCP) using Docker and Kubernetes.

## 📋 Prerequisites

Before starting, ensure you have:
- A Google Cloud Platform account
- Git installed on your local machine
- Docker installed locally (optional, for testing)
- Basic understanding of command line

## 🎯 Step-by-Step Deployment

### Step 1: Set Up Google Cloud Project

1. **Create a new GCP project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "Select a project" → "New Project"
   - Name your project (e.g., "expense-tracker-app")
   - Note down your Project ID

2. **Enable required APIs:**
   ```bash
   # Install Google Cloud CLI if you haven't already
   # Download from: https://cloud.google.com/sdk/docs/install
   
   # Login to your account
   gcloud auth login
   
   # Set your project
   gcloud config set project YOUR_PROJECT_ID
   
   # Enable required APIs
   gcloud services enable container.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

### Step 2: Create Artifact Registry

1. **Create a Docker repository:**
   ```bash
   gcloud artifacts repositories create expense-tracker \
     --repository-format=docker \
     --location=us-central1 \
     --description="Docker repository for expense tracker"
   ```

### Step 3: Create GKE Cluster

1. **Create a Kubernetes cluster:**
   ```bash
   gcloud container clusters create expense-tracker-cluster \
     --zone=us-central1-a \
     --num-nodes=2 \
     --machine-type=e2-medium \
     --enable-autoscaling \
     --min-nodes=1 \
     --max-nodes=3
   ```

2. **Get cluster credentials:**
   ```bash
   gcloud container clusters get-credentials expense-tracker-cluster --zone=us-central1-a
   ```

### Step 4: Set Up Service Account for GitHub Actions

1. **Create a service account:**
   ```bash
   gcloud iam service-accounts create github-actions-sa \
     --display-name="GitHub Actions Service Account"
   ```

2. **Grant necessary permissions:**
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/artifactregistry.writer"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/container.developer"
   ```

3. **Create and download service account key:**
   ```bash
   gcloud iam service-accounts keys create github-actions-key.json \
     --iam-account=github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

### Step 5: Configure GitHub Secrets

1. **Go to your GitHub repository**
2. **Navigate to Settings → Secrets and variables → Actions**
3. **Add the following secrets:**
   - `GCP_PROJECT_ID`: Your GCP project ID
   - `GKE_CLUSTER`: `expense-tracker-cluster`
   - `GKE_ZONE`: `us-central1-a`
   - `GCP_SA_KEY`: Copy the entire contents of `github-actions-key.json`

### Step 6: Update Kubernetes Manifests

1. **Update the deployment.yaml image path:**
   ```bash
   # Replace PROJECT_ID with your actual project ID
   sed -i 's/gcr.io\/PROJECT_ID\/expense-tracker:latest/us-central1-docker.pkg.dev\/YOUR_PROJECT_ID\/expense-tracker\/expense-tracker:latest/g' k8s/deployment.yaml
   ```

### Step 7: Deploy to GitHub

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Add Docker and Kubernetes deployment files"
   git push origin main
   ```

2. **Monitor the deployment:**
   - Go to your GitHub repository
   - Click on "Actions" tab
   - Watch the "Build and Deploy to GCP" workflow

### Step 8: Access Your Application

1. **Get the external IP:**
   ```bash
   kubectl get service expense-tracker
   ```

2. **Open your application:**
   - Copy the EXTERNAL-IP from the output
   - Open `http://EXTERNAL-IP` in your browser
   - You should see the noVNC interface with your Expense Tracker app

## 🔧 Local Testing (Optional)

Before deploying to GCP, you can test locally:

1. **Build the Docker image:**
   ```bash
   docker build -t expense-tracker .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8080:8080 expense-tracker
   ```

3. **Access locally:**
   - Open `http://localhost:8080` in your browser

## 📊 Monitoring and Logs

### View Application Logs
```bash
kubectl logs -f deployment/expense-tracker
```

### Check Pod Status
```bash
kubectl get pods
kubectl describe pod POD_NAME
```

### Scale Your Application
```bash
kubectl scale deployment expense-tracker --replicas=3
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Image pull errors:**
   - Check if the image exists in Artifact Registry
   - Verify service account permissions

2. **Pod not starting:**
   - Check logs: `kubectl logs POD_NAME`
   - Verify resource limits

3. **External IP not assigned:**
   - Wait a few minutes for LoadBalancer provisioning
   - Check if you have sufficient quota

4. **Application not accessible:**
   - Verify the service is running: `kubectl get svc`
   - Check if the pod is ready: `kubectl get pods`

### Useful Commands:

```bash
# Check cluster status
kubectl cluster-info

# View all resources
kubectl get all

# Delete deployment (if needed)
kubectl delete -f k8s/

# Restart deployment
kubectl rollout restart deployment/expense-tracker
```

## 💰 Cost Optimization

- **Use preemptible nodes** for development:
  ```bash
  gcloud container clusters create expense-tracker-cluster \
    --preemptible \
    --zone=us-central1-a
  ```

- **Set up cluster autoscaling** to scale down when not in use
- **Monitor costs** in the GCP Console under Billing

## 🔄 Updating Your Application

1. **Make changes to your code**
2. **Commit and push to main branch**
3. **GitHub Actions will automatically:**
   - Build a new Docker image
   - Push to Artifact Registry
   - Deploy to GKE

## 🗑️ Cleanup

To avoid charges, clean up resources when done:

```bash
# Delete the cluster
gcloud container clusters delete expense-tracker-cluster --zone=us-central1-a

# Delete the Artifact Registry
gcloud artifacts repositories delete expense-tracker --location=us-central1

# Delete the service account
gcloud iam service-accounts delete github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## 🎉 Congratulations!

Your Expense Tracker is now running on Google Cloud Platform! You can access it from anywhere in the world through the external IP address.

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the GitHub Actions logs
3. Check Kubernetes logs and events
4. Verify your GCP billing and quotas

Happy expense tracking! 💰📊
