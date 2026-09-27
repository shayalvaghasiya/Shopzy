# Define the set of interface endpoint services
locals {
    interface_endpoint_services = toset([
        "ecr.api",
        "ecr.dkr",
        "logs",
        "secretsmanager",
    ])
}

resource "aws_vpc_endpoint" "s3" {
    vpc_id = var.vpc_id
    service_name = "com.amazonaws.${var.aws_region}.s3"
    vpc_endpoint_type = "Gateway"

    route_table_ids = var.private_app_route_table_ids

    tags = merge(
        var.tags,
        {
            Name = "${var.name_prefix}-s3-vpce"
        }
    )
}

resource "aws_vpc_endpoint" "interface" {
    for_each = local.interface_endpoint_services

    vpc_id = var.vpc_id
    service_name = "com.amazonaws.${var.aws_region}.${each.value}"
    vpc_endpoint_type = "Interface"

    subnet_ids = var.private_app_subnet_ids
    security_group_ids = [var.endpoint_security_group_id]
    private_dns_enabled = true

    tags = merge(
        var.tags,
        {
            Name = "${var.name_prefix}-${replace(each.value, ".", "-")}-vpce"
            Service = each.value
        }
    )
}