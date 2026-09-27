output "s3_endpoint_id" {
  description = "The ID of the S3 VPC endpoint"
  value       = aws_vpc_endpoint.s3.id
}

output "interface_endpoint_ids" {
  description = "The IDs of the interface VPC endpoints"
  value       = { for service, endpoint in aws_vpc_endpoint.interface : 
  service => endpoint.id }
}