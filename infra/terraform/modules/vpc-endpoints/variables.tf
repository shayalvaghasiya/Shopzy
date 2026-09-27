variable "name_prefix" {
    type = string
}

variable "aws_region" {
    type = string
}

variable "vpc_id" {
    type = string
}

variable "private_app_subnet_ids" {
    description = "List of private subnet IDs for the application"
    type = list(string)
}

variable "private_app_route_table_ids" {
    description = "List of private route table IDs for the application"
    type = list(string)
}

variable "endpoint_security_group_id" {
    description = "List of private security group IDs for the application"
    type = string
}

variable "tags" {
    description = "A map of tags to assign to the resources"
    type = map(string)
    default = {}
}
