terraform {
    backend "s3" {
        bucket = "shopzy-terraform-state-073712114731-ap-south-1"
        key = "shopzy/production/terraform.tfstate"
        region = "ap-south-1"
        encrypt = true
        use_lockfile = true
    }
}