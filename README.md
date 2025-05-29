# Python Flask CI/CD Demo

A simple Task Management API built with Flask to demonstrate CI/CD pipeline with Google Cloud Platform.

## Complete Setup Guide

### Prerequisites

- Google Cloud Platform account with billing enabled
- GitHub account
- Git installed on your local machine
- Python 3.11+ installed

## Phase 1: Google Cloud Platform Setup

### Step 1.1: Create GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a project" → "New Project"
3. Project name: `your-project-name`
4. Note down your PROJECT-ID (usually: `your-project-name-123456`)

### Step 1.2: Install Google Cloud SDK

**For Windows (PowerShell):**
```powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

**For macOS/Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
gcloud auth login
```

### Step 1.3: Configure Project Settings

⚠️ **Important: Ensure billing account is enabled before proceeding**

```bash
# Set your project ID (replace with your actual project ID)
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Verify configuration
gcloud config list
```

### Step 1.4: Enable Required APIs

```bash
# Enable all necessary APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Verify APIs are enabled
gcloud services list
```

### Step 1.5: Configure IAM Permissions

**Set user permissions:**
```bash
# Replace with your actual project ID and email
PROJECT_ID="your-project-id"
USER_EMAIL="your-email@gmail.com"

# Grant Cloud Build permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:$USER_EMAIL" \
    --role="roles/cloudbuild.builds.editor"

# Grant Cloud Run admin permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:$USER_EMAIL" \
    --role="roles/run.admin"

# Grant Storage admin permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:$USER_EMAIL" \
    --role="roles/storage.admin"

# Grant Service Account user permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:$USER_EMAIL" \
    --role="roles/iam.serviceAccountUser"
```

**Configure Cloud Build service account permissions:**
```bash
# Get project number
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Grant Cloud Build service account permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/storage.admin"
```

## Phase 2: Deployment

### Step 2.1: Initial Deployment

```bash
# Deploy to Google Cloud
gcloud builds submit --config cloudbuild.yaml .

# Allow unauthenticated access
gcloud run services add-iam-policy-binding python-cicd-app \
    --region=us-central1 \
    --member="allUsers" \
    --role="roles/run.invoker"

# Get application URL
gcloud run services describe python-cicd-app \
    --region=us-central1 \
    --format="value(status.url)"
```

## Phase 3: GitHub Integration (Automated CI/CD)

### Step 3.1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Create new repository
3. Repository name: `python-cicd-app`
4. Set as Public or Private

### Step 3.2: Push Code to GitHub

```bash
# Initialize Git repository
git init
git add .
git commit -m "Initial commit: Flask CI/CD app"
git branch -M main

# Connect to your GitHub repository
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/python-cicd-app.git
git push -u origin main
```

### Step 3.3: Setup Automated Triggers

**Option 1: Using Google Cloud Console (Recommended)**

1. Open [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Ensure your project is selected
3. Click **"Create Trigger"**
4. Select **"Connect Repository"**
5. Choose **"GitHub"**
6. Authorize Google Cloud to access your GitHub
7. Select your repository: `YOUR_GITHUB_USERNAME/python-cicd-app`
8. Configure trigger:
   - Name: `python-cicd-app-trigger`
   - Event: `Push to a branch`
   - Branch: `^main$`
   - Configuration: `Cloud Build configuration file`
   - Path: `cloudbuild.yaml`
9. Save trigger

**Option 2: Using Developer Connect (Alternative)**

1. Visit [Developer Connect](https://console.cloud.google.com/developer-connect)
2. Create connection to GitHub
3. Select region: `us-central1`
4. Authorize and connect your repository

## Project Structure

```
python-cicd-app/
├── src/
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   └── app.py          # Main Flask application
├── tests/
│   └── test_app.py     # Unit tests
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── cloudbuild.yaml    # CI/CD pipeline configuration
└── README.md          # This file
```

## Features

- **Task Management API**: Create, read, update, delete tasks
- **Web Interface**: Simple HTML interface to view tasks
- **Health Check**: Endpoint for monitoring application health
- **Automated Testing**: Unit tests with pytest
- **CI/CD Pipeline**: Automated build, test, and deployment
- **Containerized**: Docker support for consistent deployments

## API Endpoints

- `GET /` - Home page with task overview
- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `GET /health` - Health check endpoint

## Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python src/app.py

# Run tests
python -m pytest tests/ -v
```

Visit: http://localhost:8080

## CI/CD Workflow

After GitHub integration is complete:

1. **Make code changes locally**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push
   ```
3. **Automatic process triggers:**
   - GitHub webhook → Cloud Build
   - Run tests
   - Build Docker image
   - Deploy to Cloud Run
   - Application automatically updates

## Troubleshooting

### Common Issues

1. **Billing not enabled**: Ensure billing account is linked to your project
2. **API not enabled**: Run the API enable commands from Step 1.4
3. **Permission denied**: Verify IAM permissions from Step 1.5
4. **Git push rejected**: Use `git pull origin main --allow-unrelated-histories` then push

