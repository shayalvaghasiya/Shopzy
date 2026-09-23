output "alb_security_group_id" {
  value = aws_security_group.this.id
}

output "api_gateway_security_group_id" {
  value = aws_security_group.api_gateway.id
}

output "services_security_group_id" {
  value = aws_security_group.services.id
}

output "rds_security_group_id" {
  value = aws_security_group.rds.id
}

output "vpc_endpoints_security_group_id" {
  value = aws_security_group.vpc_endpoints.id
}