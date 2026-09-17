variable "project_name" {
  type    = string
  default = "shopzy"
}

variable "environment" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "vpc_cidr" {
  type = string
}