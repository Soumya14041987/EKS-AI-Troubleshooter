output "cluster_service_role_arn" {
  description = "EKS cluster service role ARN"
  value       = aws_iam_role.cluster_service_role.arn
}

output "node_group_role_arn" {
  description = "EKS node group role ARN"
  value       = aws_iam_role.node_group_role.arn
}