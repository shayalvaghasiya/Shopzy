variable "name_prefix" {
    description = "Prefix used to name security groups"
    type = string
}

variable "vpc_id" {
    description = "ID of the VPC where security groups will be created"
    type = string
}

variable "tags" {
    description = "Additional tags for all security groups"
    type = map(string)
    default = {}
}