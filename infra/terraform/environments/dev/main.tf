module "vpc" {
  source = "../../modules/vpc"

  name               = "${var.project_name}-${var.environment}"
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones

  public_subnet_cidrs      = var.public_subnet_cidrs
  private_app_subnet_cidrs = var.private_app_subnet_cidrs
  private_db_subnet_cidrs  = var.private_db_subnet_cidrs

  tags = {
    Environment = var.environment
  }
}

module "security_groups" {
  source = "../../modules/security-groups"

  name_prefix = "${var.project_name}-${var.environment}"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Environment = var.environment
  }
}

module "vpc_endpoints" {
  source = "../../modules/vpc-endpoints"

  name_prefix = "${var.project_name}-${var.environment}"
  aws_region  = var.aws_region
  vpc_id      = module.vpc.vpc_id

  private_app_subnet_ids      = module.vpc.private_app_subnet_ids
  private_app_route_table_ids = module.vpc.private_app_route_table_ids
  endpoint_security_group_id  = module.security_groups.vpc_endpoints_security_group_id

  tags = {
    Environment = var.environment
  }
}