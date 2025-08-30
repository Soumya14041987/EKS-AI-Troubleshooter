# EKS AI Troubleshooter - Deployment Guide

## Prerequisites

1. **AWS CLI** configured with appropriate permissions
2. **Terraform** >= 1.0
3. **Python 3.8+**
4. **kubectl** (will be configured automatically)

## Quick Deployment

### Option 1: Automated Deployment
```bash
./deploy.sh my-cluster-name us-west-2
```

### Option 2: Manual Deployment

#### 1. Deploy Infrastructure
```bash
cd terraform
terraform init
terraform plan -var="cluster_name=my-eks-cluster" -var="region=us-west-2"
terraform apply -var="cluster_name=my-eks-cluster" -var="region=us-west-2"
```

#### 2. Configure kubectl
```bash
aws eks update-kubeconfig --region us-west-2 --name my-eks-cluster
```

#### 3. Setup Application
```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### 4. Access Dashboard
Open http://localhost:8000 in your browser

## Configuration

### Environment Variables
```bash
export AWS_REGION=us-west-2
export CLUSTER_NAME=my-eks-cluster
export ENABLE_RAG=true
```

### Multi-Region Deployment
Deploy to multiple regions by running terraform in different directories:

```bash
# Region 1
cd terraform-us-west-2
terraform init
terraform apply -var="region=us-west-2" -var="cluster_name=cluster-west"

# Region 2  
cd terraform-us-east-1
terraform init
terraform apply -var="region=us-east-1" -var="cluster_name=cluster-east"
```

## Cost Optimization Features

- **Spot Instances**: Default node group uses spot instances
- **Minimal Node Count**: Starts with 1 node, scales to 3 max
- **Essential Add-ons Only**: VPC CNI, CoreDNS, kube-proxy
- **CloudWatch Logging**: Basic logging without expensive services

## Security Features

- **IAM Role-based Access**: Secure cluster access
- **VPC with Private Subnets**: Nodes in private subnets
- **Security Groups**: Minimal required access
- **API Token Authentication**: Secure API endpoints

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   aws sts get-caller-identity  # Check AWS credentials
   ```

2. **Terraform State Lock**
   ```bash
   terraform force-unlock <lock-id>
   ```

3. **kubectl Connection Issues**
   ```bash
   aws eks update-kubeconfig --region <region> --name <cluster-name>
   ```

### Cleanup
```bash
cd terraform
terraform destroy -var="cluster_name=my-eks-cluster" -var="region=us-west-2"
```

## Monitoring & Logs

- **CloudWatch**: Cluster and application logs
- **Kubernetes Events**: Real-time cluster events
- **Pod Logs**: Live streaming via WebSocket
- **Resource Metrics**: CPU/Memory usage tracking

## API Endpoints

- `GET /` - Dashboard
- `POST /api/connect` - Connect to cluster
- `POST /api/analyze` - Analyze cluster
- `GET /api/pods/{namespace}` - List pods
- `GET /api/rag/query` - Query RAG knowledge base
- `WebSocket /ws/logs/{namespace}/{pod}` - Stream logs