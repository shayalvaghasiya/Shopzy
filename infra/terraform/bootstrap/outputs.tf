output "terraform_state_bucket_name" {
  description = "bucket name for state files"
  value       = aws_s3_bucket.terraform_state.bucket
}

output "terraform_state_bucket_arn" {
  description = "ARN for terraform state bucket"
  value       = aws_s3_bucket.terraform_state.arn
}