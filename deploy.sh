#!/bin/bash

set -e

echo "🚀 EKS AI Troubleshooter Deployment Script"
echo "==========================================="

# Check if required tools are installed
check_dependencies() {
    echo "Checking dependencies..."
    
    if ! command -v terraform &> /dev/null; then
        echo "❌ Terraform not found. Please install Terraform."
        exit 1
    fi
    
    if ! command -v aws &> /dev/null; then
        echo "❌ AWS CLI not found. Please install AWS CLI."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 not found. Please install Python3."
        exit 1
    fi
    
    echo "✅ All dependencies found"
}

# Deploy infrastructure
deploy_infrastructure() {
    echo "Deploying EKS infrastructure..."
    
    cd terraform
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -var="cluster_name=${CLUSTER_NAME}" -var="region=${AWS_REGION}"
    
    # Apply deployment
    terraform apply -auto-approve -var="cluster_name=${CLUSTER_NAME}" -var="region=${AWS_REGION}"
    
    # Update kubeconfig
    aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}
    
    cd ..
    echo "✅ Infrastructure deployed successfully"
}

# Setup Python application
setup_application() {
    echo "Setting up AI Troubleshooter application..."
    
    cd app
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    echo "✅ Application setup complete"
    echo "To start the application, run:"
    echo "cd app && source venv/bin/activate && python main.py"
}

# Main deployment flow
main() {
    # Set default values
    CLUSTER_NAME=${1:-"eks-ai-troubleshooter"}
    AWS_REGION=${2:-"us-west-2"}
    
    echo "Cluster Name: ${CLUSTER_NAME}"
    echo "AWS Region: ${AWS_REGION}"
    echo ""
    
    check_dependencies
    deploy_infrastructure
    setup_application
    
    echo ""
    echo "🎉 Deployment Complete!"
    echo "======================"
    echo "1. Infrastructure deployed to AWS"
    echo "2. Application ready to start"
    echo ""
    echo "Next steps:"
    echo "1. cd app && source venv/bin/activate"
    echo "2. python main.py"
    echo "3. Open http://localhost:8000 in your browser"
    echo ""
    echo "To connect to your cluster:"
    echo "- Cluster Name: ${CLUSTER_NAME}"
    echo "- Region: ${AWS_REGION}"
}

# Run main function with all arguments
main "$@"