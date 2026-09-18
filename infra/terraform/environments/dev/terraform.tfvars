environment = "dev"
vpc_cidr    = "10.10.0.0/16"

availability_zones = [
  "ap-south-1a",
  "ap-south-1b"
]

public_subnet_cidrs = [
  "10.10.0.0/24",
  "10.10.1.0/24"
]

private_app_subnet_cidrs = [
  "10.10.10.0/24",
  "10.10.11.0/24"
]

private_db_subnet_cidrs = [
  "10.10.20.0/24",
  "10.10.21.0/24"
]