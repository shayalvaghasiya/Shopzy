variable "project_name" {
  description = "short name for resource naming"
  type        = string
  default     = "shopzy"
}

variable "aws_region" {
  description = "aws region for shopzy workload"
  type        = string
  default     = "ap-south-1"
}