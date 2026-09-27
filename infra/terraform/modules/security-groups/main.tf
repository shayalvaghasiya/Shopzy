# defining security groups for the ALB, API gateway, backend services, RDS, and VPC endpoints

resource "aws_security_group" "this" {
  name        = "${var.name_prefix}-alb-sg"
  description = "Allow public web traffic to the ALB"
  vpc_id      = var.vpc_id

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-alb-sg"
  })
}

resource "aws_security_group" "api_gateway" {
    name = "${var.name_prefix}-api-gateway-sg"
    description = "Allow traffic from the ALB to the API gateway"
    vpc_id = var.vpc_id

    tags = merge(var.tags, {
        Name = "${var.name_prefix}-api-gateway-sg"
    })
}

resource "aws_security_group" "services" {
    name = "${var.name_prefix}-services-sg"
    description = "Allow internal traffic between backend services"
    vpc_id = var.vpc_id

    tags = merge(var.tags, {
        Name = "${var.name_prefix}-services-sg"
    })
}

resource "aws_security_group" "rds" {
    name = "${var.name_prefix}-rds-sg"
    description = "Allow traffic from backend services to postgres RDS"
    vpc_id = var.vpc_id

    tags = merge(var.tags, {
        Name = "${var.name_prefix}-rds-sg"
    })
}

resource "aws_security_group" "vpc_endpoints" {
    name = "${var.name_prefix}-vpc-endpoints-sg"
    description = "Allow traffic from backend services to VPC endpoints"
    vpc_id = var.vpc_id

    tags = merge(var.tags, {
        Name = "${var.name_prefix}-vpc-endpoints-sg"
    })
}



# defining security group rules for the ALB, API gateway, backend services, RDS, and VPC endpoints

# Internet -> ALB
resource "aws_vpc_security_group_ingress_rule" "alb_http" {
    security_group_id = aws_security_group.this.id
    description = "Allow HTTP traffic from the internet to the ALB"

    cidr_ipv4 = "0.0.0.0/0"
    from_port = 80
    to_port   = 80
    ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
    security_group_id = aws_security_group.this.id
    description = "Allow HTTPS traffic from the internet to the ALB"

    cidr_ipv4 = "0.0.0.0/0"
    from_port = 443
    to_port   = 443
    ip_protocol = "tcp"
}


# ALB -> API Gateway
resource "aws_vpc_security_group_egress_rule" "alb_to_api_gateway" {
    security_group_id = aws_security_group.this.id
    referenced_security_group_id = aws_security_group.api_gateway.id
    description = "Allow traffic from the ALB to the API gateway"

    from_port = 8000
    to_port   = 8000
    ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "api_gateway_from_alb" {
  security_group_id            = aws_security_group.api_gateway.id
  referenced_security_group_id = aws_security_group.this.id
  description                  = "Allow API traffic from ALB only."

  from_port   = 8000
  to_port     = 8000
  ip_protocol = "tcp"
}


# API Gateway -> internal services
resource "aws_vpc_security_group_egress_rule" "api_gateway_to_services" {
  security_group_id            = aws_security_group.api_gateway.id
  referenced_security_group_id = aws_security_group.services.id
  description                  = "Allow API Gateway to reach backend services."

  from_port   = 8001
  to_port     = 8006
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "services_from_api_gateway" {
  security_group_id            = aws_security_group.services.id
  referenced_security_group_id = aws_security_group.api_gateway.id
  description                  = "Allow backend traffic from API Gateway."

  from_port   = 8001
  to_port     = 8006
  ip_protocol = "tcp"
}

# Service -> service, required for order/payment/inventory interactions

resource "aws_vpc_security_group_ingress_rule" "services_from_services" {
  security_group_id            = aws_security_group.services.id
  referenced_security_group_id = aws_security_group.services.id
  description                  = "Allow internal Shopzy service-to-service traffic."

  from_port   = 8001
  to_port     = 8006
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "services_to_services" {
  security_group_id            = aws_security_group.services.id
  referenced_security_group_id = aws_security_group.services.id
  description                  = "Allow outbound internal Shopzy service traffic."

  from_port   = 8001
  to_port     = 8006
  ip_protocol = "tcp"
}

# Services -> RDS

resource "aws_vpc_security_group_egress_rule" "services_to_rds" {
  security_group_id            = aws_security_group.services.id
  referenced_security_group_id = aws_security_group.rds.id
  description                  = "Allow PostgreSQL connections to RDS."

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_services" {
  security_group_id            = aws_security_group.rds.id
  referenced_security_group_id = aws_security_group.services.id
  description                  = "Allow PostgreSQL only from Shopzy service tasks."

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}

# API Gateway and services -> interface VPC endpoints

resource "aws_vpc_security_group_egress_rule" "api_gateway_to_vpc_endpoints" {
  security_group_id            = aws_security_group.api_gateway.id
  referenced_security_group_id = aws_security_group.vpc_endpoints.id
  description                  = "Allow API Gateway to use AWS interface endpoints."

  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "services_to_vpc_endpoints" {
  security_group_id            = aws_security_group.services.id
  referenced_security_group_id = aws_security_group.vpc_endpoints.id
  description                  = "Allow backend services to use AWS interface endpoints."

  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "vpc_endpoints_from_api_gateway" {
  security_group_id            = aws_security_group.vpc_endpoints.id
  referenced_security_group_id = aws_security_group.api_gateway.id
  description                  = "Allow HTTPS from API Gateway."

  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "vpc_endpoints_from_services" {
  security_group_id            = aws_security_group.vpc_endpoints.id
  referenced_security_group_id = aws_security_group.services.id
  description                  = "Allow HTTPS from backend services."

  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}
