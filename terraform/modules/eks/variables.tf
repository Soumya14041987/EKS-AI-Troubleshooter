variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for EKS cluster"
  type        = list(string)
}

variable "cluster_service_role" {
  description = "EKS cluster service role ARN"
  type        = string
}

variable "node_group_role" {
  description = "EKS node group role ARN"
  type        = string
}

variable "instance_types" {
  description = "Instance types for node group"
  type        = list(string)
}

variable "capacity_type" {
  description = "Capacity type for node group"
  type        = string
}

variable "desired_size" {
  description = "Desired number of nodes"
  type        = number
}

variable "max_size" {
  description = "Maximum number of nodes"
  type        = number
}

variable "min_size" {
  description = "Minimum number of nodes"
  type        = number
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
}