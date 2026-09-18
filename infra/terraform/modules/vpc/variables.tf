variable "name" {
    description = "base name for network resources"
    type = string
}

variable "vpc_cidr" {
    description = "CIDR block for the VPC"
    type = string
}

variable "availability_zones" {
    description = "availability zones used by VPC"
    type = list(string)
}

variable "public_subnet_cidrs" {
    description = "CIDR blcoks for public subnets"
    type = list(string)

    validation {
        condition = length(var.public_subnet_cidrs) == length(var.availability_zones)
        error_message = "Provide one public subnet CIDR for each availability zone"
    }
}

variable "private_app_subnet_cidrs" {
    description = "CIDR blcoks for private subnets"
    type = list(string)

    validation {
        condition = length(var.private_app_subnet_cidrs) == length(var.availability_zones)
        error_message = "Provide one private subnet CIDR for each availability zone"
    }
}

variable "private_db_subnet_cidrs" {
    description = "CIDR blocks for private database subnets"
    type = list(string)

    validation {
        condition = length(var.private_db_subnet_cidrs) == length(var.availability_zones)
        error_message = "Provide one private database subnet CIDR for each availability zone"
    }
}

variable "tags" {
    description = "Additional tags for all VPC resources"
    type = map(string)
    
}