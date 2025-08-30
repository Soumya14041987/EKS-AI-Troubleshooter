# 🤖 EKS AI Troubleshooter - Intelligent Kubernetes Assistant

<div align="center">

![EKS AI Troubleshooter](https://img.shields.io/badge/EKS-AI%20Troubleshooter-orange?style=for-the-badge&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Terraform](https://img.shields.io/badge/Terraform-1.0+-purple?style=for-the-badge&logo=terraform)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=for-the-badge&logo=fastapi)

**🚀 Deploy in 5 minutes | 💰 Under $15/month | 🧠 RAG-Enhanced Knowledge Base**

[🎯 Quick Start](#-quick-start) • [🏗️ Architecture](#️-architecture) • [💡 Features](#-features) • [🌐 Live Demo](#-live-demo)

</div>

---

## 🌟 What is EKS AI Troubleshooter?

An intelligent, cost-effective Kubernetes troubleshooting companion that combines **real-time cluster monitoring**, **AI-powered issue detection**, and **RAG-enhanced knowledge base** to provide instant, expert-level guidance for your EKS clusters.

### ✨ Key Highlights

- 🔍 **Smart Issue Detection** - Automatically identifies CrashLoopBackOff, OOMKilled, failed deployments
- 🧠 **RAG-Enhanced AI** - Leverages official Kubernetes & AWS documentation for accurate solutions
- 💰 **Ultra Cost-Effective** - Complete solution under $15/month using spot instances
- ⚡ **Real-Time Monitoring** - Live pod logs, cluster events, and resource metrics
- 🌐 **Web-Based Dashboard** - Beautiful, responsive interface accessible from anywhere
- 🔧 **One-Click Deployment** - Fully automated infrastructure setup with Terraform

---

## 🎯 Quick Start

### Prerequisites
- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Python 3.8+

### 🚀 Deploy Everything (5 minutes)

```bash
# Clone the repository
git clone https://github.com/Soumya14041987/EKS-AI-Troubleshooter.git
cd EKS-AI-Troubleshooter

# Deploy infrastructure and application
./deploy.sh my-cluster-name us-west-2

# Start the AI Assistant
cd app && source venv/bin/activate && python main.py
```

### 🌐 Access Your Dashboard
Open **http://localhost:8000** in your browser and start troubleshooting!

---

## 💡 Features

<table>
<tr>
<td width="50%">

### 🔍 **Intelligent Analysis**
- **Issue Detection**: CrashLoopBackOff, OOMKilled, ImagePullBackOff
- **Resource Optimization**: CPU/Memory recommendations
- **Event Correlation**: Smart event analysis and pattern recognition
- **Predictive Insights**: Proactive issue identification

</td>
<td width="50%">

### 🧠 **RAG-Enhanced Knowledge**
- **Official Documentation**: Kubernetes & AWS knowledge base
- **Context-Aware Solutions**: Tailored recommendations
- **Best Practices**: Industry-standard troubleshooting guides
- **Real-Time Updates**: Always current information

</td>
</tr>
<tr>
<td width="50%">

### ⚡ **Real-Time Monitoring**
- **Live Log Streaming**: WebSocket-based pod logs
- **Cluster Health**: Real-time status monitoring
- **Resource Metrics**: CPU, memory, and storage tracking
- **Multi-Cluster Support**: Manage multiple EKS clusters

</td>
<td width="50%">

### 💰 **Cost Optimization**
- **Spot Instances**: 70% cost savings on compute
- **Minimal Infrastructure**: Essential components only
- **Auto-Scaling**: Scale down when not needed
- **Budget Alerts**: Stay within $15/month limit

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │────│  FastAPI Backend │────│ Kubernetes API  │
│   (HTML/JS)     │    │   (Python)      │    │   (EKS Cluster) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌────────┴────────┐
                       │                 │
                ┌──────▼──────┐   ┌──────▼──────┐
                │ RAG Engine  │   │ AI Analyzer │
                │ (Knowledge) │   │ (Detection) │
                └─────────────┘   └─────────────┘
                       │
                ┌──────▼──────┐
                │  Terraform  │
                │ (AWS Infra) │
                └─────────────┘
```

### 🔧 Technology Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: FastAPI, Python 3.8+
- **Infrastructure**: Terraform, AWS EKS
- **AI/ML**: RAG with sentence transformers
- **Monitoring**: Kubernetes API, CloudWatch
- **Security**: IAM roles, VPC, encrypted secrets

---

## 🌐 Live Demo

### Dashboard Overview
```
🖥️  EKS AI Troubleshooter Dashboard
┌─────────────────────────────────────────────────────────────┐
│ 🔗 Cluster Connection    │ 📊 Cluster Analysis              │
│ ┌─────────────────────┐  │ ┌─────────────────────────────┐   │
│ │ Cluster: my-eks     │  │ │ Status: ✅ Healthy          │   │
│ │ Region: us-west-2   │  │ │ Pods: 12 Running, 0 Failed │   │
│ │ Status: Connected   │  │ │ Issues: 2 Detected         │   │
│ └─────────────────────┘  │ └─────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│ 🚨 Issues Detected                                          │
│ • CrashLoopBackOff: nginx-pod (High Priority)              │
│ • OOMKilled: api-server (Critical)                         │
├─────────────────────────────────────────────────────────────┤
│ 🤖 AI Recommendations                                       │
│ • Increase memory limit for api-server to 512Mi            │
│ • Check nginx configuration for startup errors             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Options

### Option 1: Automated Deployment (Recommended)
```bash
./deploy.sh my-cluster us-west-2
```

### Option 2: Manual Deployment
```bash
# Deploy infrastructure
cd terraform
terraform init
terraform apply -var="cluster_name=my-eks" -var="region=us-west-2"

# Setup application
cd ../app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Option 3: Docker Deployment
```bash
docker build -t eks-ai-troubleshooter .
docker run -p 8000:8000 eks-ai-troubleshooter
```

---

## 💰 Cost Breakdown (Under $15/month)

| Component | Cost/Month | Description |
|-----------|------------|-------------|
| EKS Control Plane | $7.20 | Managed Kubernetes control plane |
| EC2 Spot Instances | $3-5 | t3.medium spot instances (1-2 nodes) |
| CloudWatch Logs | $1-2 | Basic logging and monitoring |
| Data Transfer | $0.50 | Minimal data transfer costs |
| **Total** | **~$12-15** | **Complete solution** |

### 💡 Cost Optimization Features
- ✅ Spot instances (70% savings)
- ✅ Auto-scaling (scale to zero when idle)
- ✅ Minimal node groups (1-3 nodes max)
- ✅ Essential add-ons only
- ✅ CloudWatch instead of expensive monitoring

---

## 🧠 RAG Knowledge Base

The AI Troubleshooter includes a comprehensive RAG (Retrieval-Augmented Generation) system that:

- 📚 **Ingests Official Documentation** from Kubernetes and AWS
- 🔍 **Semantic Search** for relevant troubleshooting information
- 🎯 **Context-Aware Responses** based on your specific cluster issues
- 🔄 **Auto-Updates** knowledge base with latest documentation

### Knowledge Sources
- Kubernetes Official Documentation
- AWS EKS Best Practices
- Troubleshooting Guides
- Community Solutions
- Error Pattern Database

---

## 🛡️ Security Features

- 🔐 **IAM Role-Based Access** - Secure cluster authentication
- 🌐 **VPC with Private Subnets** - Network isolation
- 🔑 **API Token Authentication** - Secure API endpoints
- 📝 **Audit Logging** - Complete activity tracking
- 🛡️ **Security Groups** - Minimal required access

---

## 📈 Monitoring & Observability

- 📊 **Real-Time Metrics** - CPU, memory, disk usage
- 📋 **Event Correlation** - Smart event analysis
- 🔍 **Log Aggregation** - Centralized log management
- 🚨 **Alert Integration** - Slack, email notifications
- 📈 **Trend Analysis** - Historical performance data

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/Soumya14041987/EKS-AI-Troubleshooter.git
cd EKS-AI-Troubleshooter
pip install -r app/requirements-dev.txt
pre-commit install
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- 📖 **Documentation**: [Wiki](https://github.com/Soumya14041987/EKS-AI-Troubleshooter/wiki)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Soumya14041987/EKS-AI-Troubleshooter/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Soumya14041987/EKS-AI-Troubleshooter/discussions)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for the Kubernetes community

[🚀 Get Started](#-quick-start) • [📖 Documentation](https://github.com/Soumya14041987/EKS-AI-Troubleshooter/wiki) • [🤝 Contribute](#-contributing)

</div>