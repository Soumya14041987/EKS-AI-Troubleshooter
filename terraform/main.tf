terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

data "aws_availability_zones" "available" {
  state = "available"
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  cluster_name = var.cluster_name
  vpc_cidr     = var.vpc_cidr
  azs          = slice(data.aws_availability_zones.available.names, 0, 2)
  tags         = var.tags
}

# IAM Module
module "iam" {
  source = "./modules/iam"
  
  cluster_name = var.cluster_name
  tags         = var.tags
}

# EKS Module
module "eks" {
  source = "./modules/eks"
  
  cluster_name           = var.cluster_name
  subnet_ids             = module.vpc.private_subnet_ids
  cluster_service_role   = module.iam.cluster_service_role_arn
  node_group_role        = module.iam.node_group_role_arn
  instance_types         = var.node_group_instance_types
  capacity_type          = var.node_group_capacity_type
  desired_size           = var.node_group_desired_size
  max_size               = var.node_group_max_size
  min_size               = var.node_group_min_size
  tags                   = var.tags
}