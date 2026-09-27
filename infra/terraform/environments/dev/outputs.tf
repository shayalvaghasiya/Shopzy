output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_app_subnet_ids" {
  value = module.vpc.private_app_subnet_ids
}

output "private_db_subnet_ids" {
  value = module.vpc.private_db_subnet_ids
}

output "security_group_ids" {
  value = {
    alb           = module.security_groups.alb_security_group_id
    api_gateway   = module.security_groups.api_gateway_security_group_id
    services      = module.security_groups.services_security_group_id
    vpc_endpoints = module.security_groups.vpc_endpoints_security_group_id
    rds           = module.security_groups.rds_security_group_id
  }
}