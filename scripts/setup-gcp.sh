#!/bin/bash

# GCP Setup Script for Expense Tracker
# This script helps you set up all the necessary GCP resources

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
check_gcloud() {
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud CLI is not installed. Please install it first:"
        echo "https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    print_success "Google Cloud CLI is installed"
}

# Get project ID
get_project_id() {
    if [ -z "$PROJECT_ID" ]; then
        echo -n "Enter your GCP Project ID: "
        read PROJECT_ID
    fi
    
    if [ -z "$PROJECT_ID" ]; then
        print_error "Project ID is required"
        exit 1
    fi
    
    print_status "Using Project ID: $PROJECT_ID"
}

# Set project
set_project() {
    print_status "Setting project to $PROJECT_ID"
    gcloud config set project $PROJECT_ID
    print_success "Project set to $PROJECT_ID"
}

# Enable required APIs
enable_apis() {
    print_status "Enabling required APIs..."
    
    gcloud services enable container.googleapis.com
    gcloud services enable artifactregistry.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    
    print_success "APIs enabled successfully"
}

# Create Artifact Registry
create_artifact_registry() {
    print_status "Creating Artifact Registry repository..."
    
    gcloud artifacts repositories create expense-tracker \
        --repository-format=docker \
        --location=us-central1 \
        --description="Docker repository for expense tracker" || {
        print_warning "Repository might already exist, continuing..."
    }
    
    print_success "Artifact Registry repository created"
}

# Create GKE cluster
create_gke_cluster() {
    print_status "Creating GKE cluster (this may take 5-10 minutes)..."
    
    gcloud container clusters create expense-tracker-cluster \
        --zone=us-central1-a \
        --num-nodes=2 \
        --machine-type=e2-medium \
        --enable-autoscaling \
        --min-nodes=1 \
        --max-nodes=3 \
        --disk-size=20GB \
        --disk-type=pd-standard || {
        print_warning "Cluster might already exist, continuing..."
    }
    
    print_success "GKE cluster created"
}

# Get cluster credentials
get_credentials() {
    print_status "Getting cluster credentials..."
    gcloud container clusters get-credentials expense-tracker-cluster --zone=us-central1-a
    print_success "Cluster credentials obtained"
}

# Create service account
create_service_account() {
    print_status "Creating service account for GitHub Actions..."
    
    gcloud iam service-accounts create github-actions-sa \
        --display-name="GitHub Actions Service Account" || {
        print_warning "Service account might already exist, continuing..."
    }
    
    print_success "Service account created"
}

# Grant permissions
grant_permissions() {
    print_status "Granting necessary permissions..."
    
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
        --role="roles/artifactregistry.writer"
    
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com" \
        --role="roles/container.developer"
    
    print_success "Permissions granted"
}

# Create service account key
create_service_account_key() {
    print_status "Creating service account key..."
    
    gcloud iam service-accounts keys create github-actions-key.json \
        --iam-account=github-actions-sa@$PROJECT_ID.iam.gserviceaccount.com
    
    print_success "Service account key created: github-actions-key.json"
    print_warning "Keep this file secure and add it to GitHub Secrets!"
}

# Display next steps
show_next_steps() {
    print_success "GCP setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. Add the following secrets to your GitHub repository:"
    echo "   - GCP_PROJECT_ID: $PROJECT_ID"
    echo "   - GKE_CLUSTER: expense-tracker-cluster"
    echo "   - GKE_ZONE: us-central1-a"
    echo "   - GCP_SA_KEY: (contents of github-actions-key.json)"
    echo ""
    echo "2. Update k8s/deployment.yaml with your project ID:"
    echo "   Replace 'gcr.io/PROJECT_ID' with 'us-central1-docker.pkg.dev/$PROJECT_ID/expense-tracker'"
    echo ""
    echo "3. Commit and push your changes to trigger the deployment"
    echo ""
    echo "4. Monitor the deployment in GitHub Actions"
    echo ""
    print_warning "Remember to delete github-actions-key.json after adding it to GitHub Secrets!"
}

# Main execution
main() {
    echo "🚀 GCP Setup Script for Expense Tracker"
    echo "========================================"
    echo ""
    
    check_gcloud
    get_project_id
    set_project
    enable_apis
    create_artifact_registry
    create_gke_cluster
    get_credentials
    create_service_account
    grant_permissions
    create_service_account_key
    show_next_steps
}

# Run main function
main "$@"
